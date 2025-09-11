---
author: Seth Jensen
title: "How to Download All Videos from a YouTube Channel with yt-dlp"
github_issue_number: 2147
featured:
  image_url: /blog/2025/08/how-to-download-youtube-channel/peak-in-clouds.webp
description: "Avoid data loss by using yt-dlp for high-quality archiving"
date: 2025-09-04
tags:
- tips
---

![A tall peak coated in brown and green short shrubbery, broken up only by sharp faces of rocky cliffs, sits behind wispy clouds, against an overcast backdrop. The ridgeline descends from the top left downward to the right, splitting the image in half](/blog/2025/09/how-to-download-youtube-channel/peak-in-clouds.webp)

<!-- Photo by Seth Jensen, 2023 -->

Recently, one of our clients temporarily lost access to their YouTube account to a potentially bad actor. As we met with them to regain access, we wanted to back up all their videos as quickly as possible to guarantee they retained access to over a decade of videos. Their channel had over 1000 videos, many of which were over an hour long.

The Google-approved solution here is Google Takeout, but this requires access to the Google account, meaning it wasn't an option. What's more, it only downloads in up to 720p quality (or as low as 360p, "depending on the video size")! This was unacceptable for proper archiving. It also told me I need to improve my personal Google backup process, which currently [relies on Takeout](/blog/2022/05/backing-up-your-saas-data-with-google-takeout/) 🙃.

I have used [yt-dlp](https://github.com/yt-dlp/yt-dlp) for years, so I knew it would be a good option. It's an open-source command-line tool which is perfect for this situation: you provide the URL of a YouTube video, playlist, or channel and it downloads the corresponding video(s). It's easy to automate and repeat, and is important for archival purposes, personal backups, and situations like ours. The final command we used was:

```
yt-dlp <channel URL>
```

By default, yt-dlp will download the best video and audio options available — the actual best quality available, not capped at 720p — but you can list the formats with `-F`/`--list-formats` and manually select formats with `-f`/`--format`. We first tried downloading only in mp4 format, but since it's a less storage-efficient format than webm, YouTube compresses mp4 more heavily, resulting in a lower-quality video. So we let yt-dlp choose the best option, and usually this meant webm files.

You can provide command line options via a config file in `~/.config/yt-dlp/config`, which makes it easy to automate or to run multiple times with consistent results. Here's what we set up for our download:

```
--output "%(upload_date)s - %(title)s.%(ext)s"
--download-archive archive.txt
--embed-metadata
--embed-thumbnail
--embed-subs
--all-subs
```

* We included a timestamp in the output filenames, making sorting by time easy
* `--download-archive` writes each completed file to the specified archive file (we chose `archive.txt` in whatever folder `yt-dlp` is run from) so that if you have to rerun the command it efficiently skips these videos
* `--embed-metadata` embeds metadata in the file, which is good for archiving
* `--embed-thumbnail` and `--embed-subs` will change the output muxer to something that supports embedding, like `mkv`. `--all-subs` makes sure you get all languages and implies the `--write-subs` flag

> You can also save comments using the `--write-comments` flag. They will be saved to a JSON info file for each video. You can limit the maximum number of comments to fetch with the `max_comments` argument (passed using the `--extractor-args` flag).

We were running low on disk space on the server we used, so we periodically copied all of the video files to Google Drive using [rclone](https://rclone.org/drive/) with the [move](https://rclone.org/commands/rclone_move/) subcommand.

```
rclone move --exclude='*.part' --exclude='*.txt' --progress channel-download/ gdrive:channel-drive-folder/
```

If you need to back up your YouTube videos, especially if you don't have access to your account anymore, consider using yt-dlp!
