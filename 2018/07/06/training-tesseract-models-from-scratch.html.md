Over the years, `Tesseract` has been one of the most popular OpenSource OCR solution. It's been providing ready to use models for recognizing text in many languages. Currently, there are 124 models that are available to be downloaded and used.

Not too long ago, the project's been moved in the direction of using more modern machine learning approaches and is now using [Artificial Neural Networks](https://en.wikipedia.org/wiki/Artificial_neural_network).

For some people, this move meant a lot of confusion when they wanted to train their own models. This blog post tries to explain the process of turning scans of images with textual ground-truth data into models that are ready to be used.

## Tesseract pre-trained models

You can download the pre-created ones designed to be fast and consume less memory: [https://github.com/tesseract-ocr/tessdata_fast](https://github.com/tesseract-ocr/tessdata_fast), as well as the ones requiring more in terms of resources but giving a better accuracy: [https://github.com/tesseract-ocr/tessdata_best](https://github.com/tesseract-ocr/tessdata_best).

Pre-trained models have been created using the images with text artificially rendered using a huge corpus of text coming from the web. The text was rendered using different fonts. The project's wiki states that:

> For Latin-based languages, the existing model data provided has been trained on about  [400000 textlines spanning about 4500 fonts](https://github.com/tesseract-ocr/tesseract/issues/654#issuecomment-274574951) . For other scripts, not so many fonts are available, but they have still been trained on a similar number of textlines.

## Training a new model from scratch

Before diving in, there're a couple of broader aspects you need to know:

* The latest Tesseract uses [Artificial Neural Networks](https://en.wikipedia.org/wiki/Artificial_neural_network) based models (they differ totally from the older approach)
* You might want to get familiar with how neural networks work and how their different types of layers can be used and what you can expect of them
* It's definitely a bonus to read about the "Connectionist Temporal Classification", explained brilliantly at [Sequence Modeling with CTC](https://distill.pub/2017/ctc/) (it's not mandatory though)

### Compiling the training tools

This blog post talks specifically about the latest 4* version of `Tesseract`. Please make sure that you have that installed and not some older 3* one.

To continue with the training, you'll also need the training tools. The project's wiki already explains the process of getting them well enough: [https://github.com/tesseract-ocr/tesseract/wiki/TrainingTesseract-4.00#building-the-training-tools](https://github.com/tesseract-ocr/tesseract/wiki/TrainingTesseract-4.00#building-the-training-tools). 

### Preparing the training data

Training datasets consist of `*.tif` files and accompanying `*.box` files. While the image files are easy to prepare, the box files seem to be a source of confusion.

For some images you'll want to **ensure that there's at least 10px of free space between the border and the text**. Adding it to all of the images will not hurt and will only ensure that you won't see odd looking warning messages during the training.

The first rule is that you'll have one box file per one image. You need to give them the same prefixes e. g: `image1.tif` and `image1.box`. The box files describe used characters as well as their spatial location within the image.

Each line describes one character as follows:

`<symbol> <left> <bottom> <right> <top> <page>`

Where:

* `<symbol>` is the character e.g `a` or `b`
* `<left> <bottom> <right> <top>` are the coordinates of the rectangle that fits the character on the page. Note that the coordinates system used by `Tesseract` has `(0,0)` in the bottom-left corner of the image!
* `<page>` is only relevant if you're using multi-pages `tif` files. In all other cases just put `0` in here

The order of characters is extremely important here. They **should be sorted strictly in the visual order — going from left to right**. `Tesseract` is doing the `Unicode`  bidi-re-ordering internally on its own.

Each word should be separated by the line with a space as the `<symbol>`. It works best for me to set a `1x1` small rectangle as a bounding box that follows directly the previous character.

If your image contains more than one line, the line ending should be marked with a line where `<symbol>` is a tab.

#### Generating the `unicharset` file

If you've went through the neural networks reading, you'll quickly understand that if the model is to be fast, it needs to be given a constrained list of characters you want it to recognize. Trying to make it choose out the whole `Unicode` set would be computationally unfeasible. This is what the so-called `unicharset` file is for. It defines the set of graphemes along with providing info about their basic properties.

`Tesseract` does come with its own utility for compiling that file but I've found it very buggy. That's what it looked like the last time I tried it — which was June 2018. I came up with my own script in `Ruby` which compiles a very basic version of that file and is more than enough:

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

`ruby ./extract_unicharset.rb path/to/all-boxes > path/to/unicharset`

Where to get the `all-boxes` file from? The script only cares about the unique set of characters from the box files. The following gist of shell-work will provide you with all you need:

```bash
cat path/to/dataset/*.box > path/to/all-boxes
ruby ./extract_unicharset.rb path/to/all-boxes > path/to/unicharset
```

Notice that the last command should create a `path/to/unicharset` text file for you.

#### Combining images with box files into `*.lstmf` files

The image and box files aren't being directly fed into the trainer. Instead, `Tesseract` works with the special `*.lstmf` files which combine images, boxes and text for each pair of `*.tif` and `*.box`.

In order to generate those `*.lstmf` files you'll need to run the following:

```bash
cd path/to/dataset
for file in `ls -1 *.tif`; do
  echo $file
  base=`basename $file .tif`
  tesseract $file $base lstm.train
done
```

After the above is done, you should be able to find the accompanying `*.lstmf` files. Make sure that you have `Tesseract` with `langdata`  and `tessdata` properly installed. If you keep your `tessdata` folder in a non-standard location, you might need to either export or set in-line the following shell variable:

```bash
# exporting so that it's available for all consequtive commands:
export TESSDATA_PREFIX=path/to/your/tessdata

# or run it in-line:
cd path/to/dataset
for file in `ls -1 *.tif`; do
  echo $file
  base=`basename $file .tif`
  TESSDATA_PREFIX=path/to/your/tessdata tesseract $file $base lstm.train
done
```

We'll need to generate the `all-lstmf` file containing paths to all those files that we will use later:

```bash
ls -1 *.lstmf | sort -R > all-lstmf
```

Notice the use of `sort -R` which makes the list sorted randomly which is a good practice when preparing the training data in many cases.

#### Generating the training and evaluation files lists

Next, we want to create the `list.train` and `list.eval` files. Their purpose is to contain the paths to `*.lstmf` files that `Tesseract` is going to use during the training and during the evaluation. Training and evaluation are interleaved. The former adjusts the neural network learnable parameters to minimize the so-called loss. The evaluation here is strictly to enhance the user experience: it prints out accuracy metrics periodically, letting you know how much the model has learned so far. Their values are averaged out. You can expect to see two metrics being shown: `char error` and `word error`: both are going to be close to 100% in the beginning but with all going well, you should see them dropping even to below 1%. 

The evaluation set is often called the "holdout set". How many training examples should it contain? That depends, if you have a big enough set, something around 10% of all of the examples should be more than enough. You might also not care about the training-time evaluation and set it to something very small. You'd then do your own evaluation after the network's loss converges to something small (by small we mean something close to `0.1` or less).

Assuming that you want the evaluation set to contain 1000 examples, here's how you can generate the `list.train` and `list.eval`:

```bash
cat path/to/all-lstmf | head -n  1000 > list.eval
cat path/to/all-lstmf | tail -n +1001 > list.train
```

If you'd like to express it in terms of fractions of all of the examples:

```bash
holdout_count=$(count_all=`cat path/to/all-lstmf | wc -l`; bc <<< "$count_all * 0.1 / 1")

cat path/to/all-lstmf | head -n  $holdout_count > list.eval
cat path/to/all-lstmf | tail -n +$holdout_count > list.train
```

The above shell code assigns around 10% examples to the holdout set.

#### Compiling the initial `*.traineddata` file

There's one last piece that we'll need to generate before we'll be able to start the training process: the `yourmodel.traineddata`. This file is going to contain the initial info needed for the trainer to perform the training:

```bash
combine_lang_model \
  --input_unicharset path/to/unicharset \
  --script_dir path/to/your/tessdata \
  --output_dir path/to/output \
  --lang_is_rtl \ # set it only if you work with a RTL language
  --pass_through_recoder \ # I found it working better with this option
  --lang yourmodelname
```

The above should create a bunch of files in the specified output directory.

#### Starting the actual training process

To start the training process you'll need to execute the `lstmtraining` app. It accepts the arguments that are described below.

```bash
num_classes=`head -n1 path/to/unicharset`

lstmtraining \
  path/to/traineddata-file \
  --net_spec "[1,40,0,1 Ct5,5,64 Mp3,3 Lfys128 Lbx256 Lbx256 O1c$num_classes]" \
  --model_output path/to/model/output
  --train_listfile path/to/list.train
  --eval_listfile path/to/list.eval
```

You're giving it the compiled `*.traineddata` file and the train / eval file lists and it trains the new model for you. It will adjust the neural network parameters to make the error between its predictions and what is known as ground-truth smaller and smaller.

There's one part that we haven't talked about yet: the `--net_spec` argument and its accompanying value given as string.

The neural network "spec" is there because neural networks come in many different shapes and forms. The subject is beyond the scope of this article. If you don't know anything yet but are curious, I encourage you to look for some good books. The process of learning about them is extremely rewarding — if you're into Math and Computer Science.

The value for that argument I presented above should be more than enough for most of your needs. That's unless you'd like to e. g. recognize vertical text, for which I'd recommend adjusting the spec greatly.

The format that the given string follows is called `VGSL`. You can find out more about it on the [Tesseract Wiki](https://github.com/tesseract-ocr/tesseract/wiki/VGSLSpecs).

#### Finishing the training and compiling the resulting model file

If you've got excited by what we've done so far, I have to encourage your expectations to make friends with **The Reality**. The truth is that the training process can take days — depending on how fast your machine is and how many training examples you have. You may notice it taking even longer if your examples differ by a huge factor. That might be true if you're feeding it examples that use significantly different fonts.

Once the training error rate is small enough and doesn't seem to be converging further, you may want to stop it and compile the final model file.

During the training, the `lstmtraining` app will output checkpoint files every once in a while. They are there to make it possible to stop the training and resume it later (with the `--continue_from` argument). You create the final model files out of those checkpoint files with:

```bash
lstmtraining \
  --traineddata path/to/traineddata-file \
  --continue_from path/to/model/output/checkout \
  --model_output path/to/final/output \
  --stop_training
``` 

And that's it — you can now take the output file of that last command and place it inside your `tessdata` folder it immediately `Tesseract` will be able to use it.
