Within the world of OpenSource software, the choice between different OCR platforms is not very big. There are a couple of projects being used with some success. The most notable ones are:

* Tesseract ([GitHub - tesseract-ocr/tesseract: Tesseract Open Source OCR Engine (main repository)](https://github.com/tesseract-ocr/tesseract))
* Ocropy ([GitHub - tmbdev/ocropy: Python-based tools for document analysis and OCR](https://github.com/tmbdev/ocropy))
* Kraken (Ocropy's fork - [GitHub - mittagessen/kraken: Ocropus fork with sane defaults](https://github.com/mittagessen/kraken))

## Tesseract pre-trained models

The project comes with a wide range of models, ready to be used for recognition based on pretty much any living language we have. You can download models designed to be fast and consume less memory: [GitHub - tesseract-ocr/tessdata_fast: Fast integer versions of trained models](https://github.com/tesseract-ocr/tessdata_fast), as well as the ones requiring more in terms of resources but giving a better accuracy: https://github.com/tesseract-ocr/tessdata_best.

The ones that come pre-trained have been trained using the images with text artificially rendered using a huge corpus of text coming from the web. The text was being rendered with different fonts. The project's wiki states that:

> For Latin-based languages, the existing model data provided has been trained on about  [400000 textlines spanning about 4500 fonts](https://github.com/tesseract-ocr/tesseract/issues/654#issuecomment-274574951) . For other scripts, not so many fonts are available, but they have still been trained on a similar number of textlines.

How about training new models from labelled images? The wiki isn't clear about it to this time. It's pretty easy though, once you know how it all works.

## Training a new model from scratch

Before diving in, there're a couple of broader aspects you need to know:

* The latest Tesseract uses neural networks based models (they differ totally from the older approach)
* You might want to get familiar with how neural networks work and how their different types of layers can be used and what you can expect of them
* It's definitely a bonus to read about the "Connectionist Temporal Classification", explained brilliantly at [Sequence Modeling with CTC](https://distill.pub/2017/ctc/) (it's not mandatory though)

### Preparing the training data

Training datasets consist of `*.TIF` files and accompanying `*.box` files. While the image files are straight forward to prepare, the box files seem to be a source of confusion.

#### Preparing the image files

For some images you'll want to *ensure that there's at least 10px of free space between the border and text pixels*. Adding it to all of the images will not hurt and will only ensure that you won't see odd looking warning messages during the training.

#### Preparing box files for images

The first rule is that you'll have one box file per one image. You need to give them the same prefixes e. g: `image1.tif` and `image1.box`. Next, the box files contain an info about the characters as well as their spatial location within the image. Each line describes one character as follows:

`<symbol> <left> <bottom> <right> <top> <page>`

Where:

* `<symbol>` is the character e.g `a` or `b`
* `<left> <bottom> <right> <top>` are thse coordinates of the rectangle that fits the character on the page. Note that the coordinates system used by `Tesseract` has `(0,0)` in the bottom-left corner of the image!
* `<page>` only relevant if you're using multi-pages `TIF` files. In all other cases just put `0` in here

The order of characters is extremely important here. They *should be sorted strictly in the visual order - going from left to right*. `Tesseract` is doing the `Unicode`  bidi-re-ordering internally on its own.

Each word should be separated by the line with a space as the `<symbol>`. It works best for me to set a `1x1` small rectangle as a bounding box that follows directly the previous character. E.g:

`  10 10 11 11 0` (notice two spaces at the beginning, first for the `<symbol>` and second as a field separator).

If your image contains more than one line, the line ending should be marked with a line where `<symbol>` as a tab.

#### Generating the `unicharset` file

If you've went through the neural networks reading, you'll quickly understand that if the model is to be fast, it needs to be given a constrained list of characters we want it to recognize (instead of the whole e. g. Unicode set which would computationally even be unfeasible). Part of enabling that is creating a so-called `unicharset` file.

While `Tesseract` comes with its own utility for doing so, I've found it very, very buggy (at least the last time I tried to use it - which was June 2018). I came up with my own Ruby script which works well enough:

```ruby
require "rubygems"
require "unicode/scripts"
require "unicode/categories"

bool_to_si = -> (b) {
  b ? "1" : "0"
}

is_digit = -> (props) {
  (props & ["Nd", "No", "Nl"]).count > 0
}

is_letter = -> (props) {
  (props & ["LC", "Ll", "Lm", "Lo", "Lt", "Lu"]).count > 0
}

is_alpha = -> (props) {
  is_letter.call(props)
}

is_lower = -> (props) {
  (props & ["Ll"]).count > 0
}

is_upper = -> (props) {
  (props & ["Lu"]).count > 0
}

is_punct = -> (props) {
  (props & ["Pc", "Pd", "Pe", "Pf", "Pi", "Po", "Ps"]).count > 0
}

if ARGV.length < 1
  $stderr.puts "Usage: ruby ./extract_unicharset.rb path/to/all-boxes"
  exit
end

if !File.exist?(ARGV[0])
  $stderr.puts "The all-boxes file #{ARGV[0]} doesn't exist"
  exit
end

uniqs = IO.readlines(ARGV[0]).map { |line| line[0] }.uniq.sort

outs = uniqs.each_with_index.map do |char, ix|
  script = Unicode::Scripts.scripts(char).first
  props = Unicode::Categories.categories(char)

  isalpha = is_alpha.call(props)
  islower = is_lower.call(props)
  isupper = is_upper.call(props)
  isdigit = is_digit.call(props)
  ispunctuation = is_punct.call(props)

  props = [ isalpha, islower, isupper, isdigit, ispunctuation].reverse.inject("") do |state, is|
    "#{state}#{bool_to_si.call(is)}"
  end

  "#{char} #{props.to_i(2)} #{script} #{ix + 1}"
end

puts outs.count + 1
puts "NULL 0 Common 0"
outs.each { |o| puts o }
```

You'll need to install the `unicode-scripts` and `unicode-categories` gems first. The usage is as it stands in the source code:

`ruby ./extract_unicharset.rb path/to/all-boxes`

Where to get the `all-boxes` file? The script only cares about the unique set of characters from the box files so the following will suffice:

```bash
cat path/to/dataset/*.box > path/to/all-boxes
ruby ./extract_unicharset.rb path/to/all-boxes
```

#### Combining images with box files into `*.lstmf` files

The image and box files aren't being directly fed into the trainer. Instead, `Tesseract` accepts the `*.lstmf` files which combine those both into one.

In order to generate those `*.lstmf` files you'll need to run the following:

```bash
cd path/to/dataset
for file in `ls -1 *.tif`; do
  echo $file
  base=`basename $file .tif`
  tesseract $file $base lstm.train
done
```

After the above is done, you should be able to find the accompanying `*.lstmf` files. Make sure that you have `Tesseract` with `langdata`  and `tessdata` properly installed. If you keep your `tessdata` folder in some non-standard location, you might need to either export or set in-line the following shell variable:

```bash
# exporting so that it's available for all consequtive commands:
export TESSDATA_PREFIX=path/to/your/tessdata

# or run it in-line:
TESSDATA_PREFIX=path/to/your/tessdata tesseract example1.tif example1 lstm.train
```

We'll need to generate the `all-lstmf` file containing paths to all those files that we will use later:

```bash
ls -1 *.lstmf | sort -R > all-lstmf
```

Notice the use of `sort -R` which makes the list sorted randomly which is always a good practice when preparing the training data for any machine learning project.

#### Generating the training and evaluation files lists

Next, we want to create the `list.train` and `list.eval` files. They are going to contain the paths to `*.lstmf` files we want `Tesseract` to use during the training (when the neural network's parameters are being learned) and during the evaluation (periodically when it will print out the accuracy / error statistics to let us know about the stage it is at).

The evaluation set is often called the "holdout set". How many training examples should it contain? That's a matter of finding for yourself. If you have a big enough set, something around 10% of all of the examples should be more than enough. You might also not care that much about the training time evaluation and set it to something small — and do your own evaluation after the training error (which is based on the training examples) converges to something small (by small we mean something less than `0.1`).

Assuming that you want the evaluation set to contain 1000 examples, here's how you can generate the `list.train` and `list.eval`:

```bash
cat all-lstmf | head -n  1000 > list.eval
cat all-lstmf | tail -n +1001 > list.train
```

#### Compiling the initial `*.traineddata` file

There's one last piece that we'll need to generate before we'll be able to start the training process: the `yourmodel.traineddata` that will contain the info about the charset among others:

```bash
combine_lang_model \
  --input_unicharset path/to/unicharset-file-generated-previously \
  --script_dir path/to/your/tessdata \
  --output_dir path/to/output \
  --lang_is_rtl \ # set it only if you work with a RTL language
  --pass_through_recoder \ # I found it working better with this option
  --lang yourmodelname
```

The above should create bunch of files in the specified output directory.

#### Starting the actual training process

To start the training process you'll need this last bit of a cli command:

```bash
num_classes=`head -n1 path/to/unicharset`

lstmtraining \
  path/to/traineddata-file \
  --net_spec "[1,40,0,1 Ct5,5,64 Mp3,3 Lfys128 Lbx256 Lbx256 O1c$num_classes]" \
  --model_output path/to/model/output
  --train_listfile path/to/list.train
  --eval_listfile path/to/list.eval
```

What's happening here? The `lstmtraining` is the actual model training program that comes with `Tesseract` when being compiled / installed with the training tools. You're giving it the compiled `*.traineddata` file and the train / eval file lists and it trains the new model for you. It will adjust the neural network parameters in such a way that the error between its predictions and what is given to it will be getting smaller and smaller.

If you're very focused though, you've probably noticed one argument we gave it that we haven't yet talked about: `--net_spec`.

The neural network "spec" is there because neural networks come in many different shapes and forms. The subject is beyond the scope of this article (if you don't know anything yet about it you really need thick books rather than blog posts) though I gave you a spec that will probably work for you pretty well - just because I like you :)

#### Finishing the training and compiling the resulting model file

If you've got excited by what we've done so far, I have to encourage your expectations to make friends with *the-reality*. The reality is that the training process can take days - depending on how fast your machine is and how many training examples you have. You may notice it taking even longer if your examples differ from one another by a huge factor (e. g. having texts in different fonts).

Once the training error rate is small though and doesn't seem to be converging further, you may want to stop it and compile the final model file.

During the training, the `lstmtraining` application will output checkpoint files every once in a while. They are there to make it possible to stop the training and resume it later (with the `--continue_from` argument). You create the final model files out of those checkpoint files too:

```bash
lstmtraining \
  --traineddata path/to/traineddata-file \
  --continue_from path/to/model/output/checkout \
  --model_output path/to/final/output \
  --stop_training
``` 

And that's it! You can now take the output file of that last command and place it inside your `tessdata` folder it immediately `Tesseract` will be able to use it.
