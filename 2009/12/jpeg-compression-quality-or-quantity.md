---
author: Daniel Browning
title: 'JPEG compression: quality or quantity?'
github_issue_number: 243
tags:
- browsers
- graphics
- optimization
- compression
date: 2009-12-24
---

There are many aspects of JPEG files that are interesting to web site developers, such as:

- The optimal trade off between quality and file size for any encoder and uncompressed source image.
- Reducing size of an existing JPEG image when the uncompressed source is unavailable, but still finding the same optimal trade-off.
- Comparison of different encoders and/or settings for quality at a given file size.

Two essential factors are file size and image quality. Bytes are objectively measurable, but image quality is much more nebulous. What to one person is a perfectly acceptable image is to another a grotesque abomination of artifacts. So the quality factor is subjective. For example, Steph sent me some images to compare compression artifacts. Here is the first one with three different settings in ImageMagick: 95, 50, and 8:

<table cellpadding="0" cellspacing="2">
<tbody><tr><td valign="top">
<a href="/blog/2009/12/jpeg-compression-quality-or-quantity/image-0.jpeg"><img src="/blog/2009/12/jpeg-compression-quality-or-quantity/image-0.jpeg" title="size: 27K setting: 95"/></a></td>
<td valign="top"><a href="/blog/2009/12/jpeg-compression-quality-or-quantity/image-1.jpeg"><img src="/blog/2009/12/jpeg-compression-quality-or-quantity/image-1.jpeg" title="size: 8.0K setting: 50"/></a></td>
<td valign="top">
<a href="/blog/2009/12/jpeg-compression-quality-or-quantity/image-2.jpeg"><img src="/blog/2009/12/jpeg-compression-quality-or-quantity/image-2.jpeg" title="size: 2.9K setting: 8"/></a></td></tr></tbody></table>

Compare the subtle (or otherwise) differences in the following images (mouseover shows the filesize and compression setting):

<table>
<tbody><tr>
<td><a href="/blog/2009/12/jpeg-compression-quality-or-quantity/image-3.jpeg"><img src="/blog/2009/12/jpeg-compression-quality-or-quantity/image-3.jpeg" title="size: 30K setting: 95"/></a></td>
<td><a href="/blog/2009/12/jpeg-compression-quality-or-quantity/image-4.jpeg"><img src="/blog/2009/12/jpeg-compression-quality-or-quantity/image-4.jpeg" title="size: 17K setting: 85"/></a></td>
</tr><tr>
<td><a href="/blog/2009/12/jpeg-compression-quality-or-quantity/image-5.jpeg"><img src="/blog/2009/12/jpeg-compression-quality-or-quantity/image-5.jpeg" title="size: 7.7K setting: 50"/></a></td>
<td><a href="/blog/2009/12/jpeg-compression-quality-or-quantity/image-6.jpeg"><img src="/blog/2009/12/jpeg-compression-quality-or-quantity/image-6.jpeg" title="size: 4.1K setting: 20"/></a></td>
</tr></tbody></table>

Mouseover each image for the file size and ImageMagick compression setting. Additional comparisons are below. Each image can be opened in a separate browser tab for easy A/B comparison. I think many would find the setting of 8 to have too many artifacts, even though it’s 10 times smaller than image compressed at a setting of 95. Some would find the setting of 50 to be an acceptable tradeoff between quality and size, since it sends 3.4 times fewer bytes.

Here is the code I wrote to make the comparison (shell script is great for this stuff):

```bash
#!/bin/bash
HTML_OUTFILE=comparison.html
echo '<html>' > $HTML_OUTFILE

write_img_html () {
    size=`du -h --apparent-size $1 | cut -f 1`
    if [ -n "$2" ]; then
       qual="setting: $2"
    fi
    cat <<EOF >>$HTML_OUTFILE
<a href="$1"><img src="$1" title="size: $size $qual"></a>
EOF
}

for name in image1 image2; do
    orig=$name-original.jpg
    resized=$name-300.png

    echo Resizing $orig to 300 on longest side: $resized...
    convert $orig -resize 300x300 $resized
    write_img_html $resized "lossless"

    for quality in 100 95 85 50 20 8 1; do
        echo Creating JPEG quality $quality...
        jpeg=$name-300-q-$quality.jpg
        convert $resized -strip -quality $quality $jpeg
        write_img_html $jpeg $quality
    done
done
```

Another factor that often comes into play is how artifacts in the image (e.g. aliasing, ringing, noise) combine with JPEG compression artifacts to exacerbate quality problems. So one way to get smaller file sizes is to reduce the other types of artifacts in the image, thereby allowing higher JPEG compression.

The most common source of artifacts is image resizing. If you are resizing the images, I strongly recommend using a program that has a high quality filter. Irfanview and ImageMagick are two good choices.

The ideal situation is this:

- Uncompressed source image
- Full-resolution if you will be handling the resize
- Absent artifacts such as aliasing
- Resize performed with good software like ImageMagick
- JPEG compression chosen based on subjective quality assessment.

Choosing the trade-off between quality and file size is difficult in part because it varies by image content. Images with lots of small color details (e.g. bright fabric threads; AKA high spatial frequency chroma) stand less compression than images that only have medium sized details that do not have important  and minute color information.

One of the settings that is important for small web images is removal of the color space profile (e.g. sRGB). The only time it is needed is when there is a good reason for using non-sRGB JPEG, such as when you are certain that your users will have color managed browsers. Removing it can shave off 5KB or so; software will assume images without profiles have an sRGB profile. It can be removed with the -strip parameter of ImageMagick.

As for choosing the specific compression settings, keep in mind that there are over 30 different types of options/techniques that can be used in compressing the image. Most image programs simplify that to a sliding scale from 0 to 100, 1 to 12, or something else. Keep in mind that even when programs use the same scale (e.g. 0 to 100), they probably have different ideas of what the numbers mean. 95 in one program may be very different than 95 in another.

If bandwidth is not an issue, then I use a setting of 95 on ImageMagick, because in normal images I can’t tell the difference between 95 and 100. But when file size in an important concern, I consider 85 to be the optimal setting. In this image, the difference should be clear, but I generally find that cutting filesize in half is worth it. Below 85, the artifacts are too onerous for my taste.

You don’t often hear about web site visitors’ dissatisfaction with compression artifacts, so you might be tempted to just reduce file sizes even beyond the point where it gets noticable. But I think there is a subliminal effect from the reduced image quality. Visitors may not stop visiting the site immediately, but my gut feeling is it leaves them with a certain impression in their mind or taste in their mouth. I would guess that user testing might result in comments such as “the X web site is not the same high-grade quality as the Y web site”, even if they don’t put it into words as specific as “the compression artifacts make X look uglier than Y”. Even if that pet theory is true, it still has to be balanced against the benefit of faster page loading times.

Ideally, the tradeoff between quality and page loading time would be a choice left to the user. Those who prefer fewer artifacts could set their browser to download larger, less-compressed image files than the default, while users with low bandwidth could set it for more compressed images to get a faster page load at the expense of quality. I could imagine an Apache module and corresponding Firefox add-on some day.

Regarding the situation where you want to reduce the file size of existing JPEGs, my advice is to first try (hard) to get the original source files. You can do better (for any given quality/size tradeoff) from those than you can by just manipulating the existing files. If that’s not possible, then the suboptimal workflows like jpegtran, jpegoptim, and doing a full decompress/recompress are the only alternative.

As far as comparing different encoders, I haven’t really looked into that except to compare ImageMagick and Photoshop, where I (subjectively) determined they both had about similar quality for file size (and vice-versa).

Here are all the comparison images. The file size and ImageMagick quality setting are in the rollover. I suggest opening images in browser tabs for easy A/B comparison.

<table>
<tbody><tr>
<td><a href="/blog/2009/12/jpeg-compression-quality-or-quantity/image-7.png"><img src="/blog/2009/12/jpeg-compression-quality-or-quantity/image-7.png" title="size: 87K setting: lossless"/></a></td>
<td><a href="/blog/2009/12/jpeg-compression-quality-or-quantity/image-8.jpeg"><img src="/blog/2009/12/jpeg-compression-quality-or-quantity/image-8.jpeg" title="size: 74K setting: 100"/></a></td>
<td><a href="/blog/2009/12/jpeg-compression-quality-or-quantity/image-0.jpeg"><img src="/blog/2009/12/jpeg-compression-quality-or-quantity/image-0.jpeg" title="size: 27K setting: 95"/></a></td>
<td><a href="/blog/2009/12/jpeg-compression-quality-or-quantity/image-10.jpeg"><img src="/blog/2009/12/jpeg-compression-quality-or-quantity/image-10.jpeg" title="size: 15K setting: 85"/></a></td>
</tr><tr>
<td><a href="/blog/2009/12/jpeg-compression-quality-or-quantity/image-1.jpeg"><img src="/blog/2009/12/jpeg-compression-quality-or-quantity/image-1.jpeg" title="size: 8.0K setting: 50"/></a></td>
<td><a href="/blog/2009/12/jpeg-compression-quality-or-quantity/image-12.jpeg"><img src="/blog/2009/12/jpeg-compression-quality-or-quantity/image-12.jpeg" title="size: 4.8K setting: 20"/></a></td>
<td><a href="/blog/2009/12/jpeg-compression-quality-or-quantity/image-2.jpeg"><img src="/blog/2009/12/jpeg-compression-quality-or-quantity/image-2.jpeg" title="size: 2.9K setting: 8"/></a></td>
<td><a href="/blog/2009/12/jpeg-compression-quality-or-quantity/image-14.jpeg"><img src="/blog/2009/12/jpeg-compression-quality-or-quantity/image-14.jpeg" title="size: 1.7K setting: 1"/></a></td>
</tr></tbody></table>

<table><tbody><tr>
<td><a href="/blog/2009/12/jpeg-compression-quality-or-quantity/image-15.png"><img src="/blog/2009/12/jpeg-compression-quality-or-quantity/image-15.png" title="size: 87K setting: lossless"/></a></td>
<td><a href="/blog/2009/12/jpeg-compression-quality-or-quantity/image-16.jpeg"><img src="/blog/2009/12/jpeg-compression-quality-or-quantity/image-16.jpeg" title="size: 80K setting: 100"/></a></td>
</tr><tr>
<td><a href="/blog/2009/12/jpeg-compression-quality-or-quantity/image-3.jpeg"><img src="/blog/2009/12/jpeg-compression-quality-or-quantity/image-3.jpeg" title="size: 30K setting: 95"/></a></td>
<td><a href="/blog/2009/12/jpeg-compression-quality-or-quantity/image-4.jpeg"><img src="/blog/2009/12/jpeg-compression-quality-or-quantity/image-4.jpeg" title="size: 17K setting: 85"/></a></td>
</tr><tr>
<td><a href="/blog/2009/12/jpeg-compression-quality-or-quantity/image-5.jpeg"><img src="/blog/2009/12/jpeg-compression-quality-or-quantity/image-5.jpeg" title="size: 7.7K setting: 50"/></a></td>
<td><a href="/blog/2009/12/jpeg-compression-quality-or-quantity/image-6.jpeg"><img src="/blog/2009/12/jpeg-compression-quality-or-quantity/image-6.jpeg" title="size: 4.1K setting: 20"/></a></td>
</tr><tr>
<td><a href="/blog/2009/12/jpeg-compression-quality-or-quantity/image-21.jpeg"><img src="/blog/2009/12/jpeg-compression-quality-or-quantity/image-21.jpeg" title="size: 2.2K setting: 8"/></a></td>
<td><a href="/blog/2009/12/jpeg-compression-quality-or-quantity/image-22.jpeg"><img src="/blog/2009/12/jpeg-compression-quality-or-quantity/image-22.jpeg" title="size: 1.3K setting: 1"/></a></td>
</tr></tbody></table>
