---
title: "OpenITI Starts Arabic-script OCR Catalyst Project"
author: Elizabeth Garrett Christensen
tags: clients, machine-learning, natural-language-processing
gh_issue_number: 1555
---

<img src="/blog/2019/09/10/openiti-arabic-ocr-catalyst-project/banner.jpg" alt="Decorative Arabic calligraphy" /> [Photo](https://www.flickr.com/photos/firaskaheel/16680667070) by Free Quran Pictures 4K, cropped, [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/)

Congratulations to the [Open Islamicate Texts Initiative](https://iti-corpus.github.io/) (OpenITI) on their new project the Arabic-script OCR Catalyst Project (AOCP)! This project received funding from the The Andrew W. Mellon Foundation this summer.

End Point developer Kamil Ciemniewski will be serving the project as a Technology Integration Specialist. Kamil has been involved with OpenITI since 2018 and with the affiliated project, [Corpus Builder](https://openiti.org/projects/corpusbuilder), since 2017.

Corpus Builder project version 1.0 made collaborative effort possible in producing ground truth datasets for OCR models training. The application acts as a versioned database of text transcriptions and a full OCR pipeline itself. The versioned character of the database follows closely the model used by Git.

What is remarkable about it is that it brings the ability to work on revisions of documents whose character isn’t linear as text in the Git case. For the OCR problem, one needs both textual data but also the spatial: where exactly the text is to be found.

A sophisticated mechanism of applying updates to those documents minimizes (with mathematical guarantees) the chance of introducing merge conflicts.

The project also hosts a great-looking UI interface allowing non-technical editors to work within the workflow of this versioned data.

CorpusBuilder works with both [Tesseract](https://github.com/tesseract-ocr/tesseract) and [Kraken](http://kraken.re/) as its OCR backends and is capable of exporting datasets in their respective formats for further model training / retraining. Training of Tesseract models was covered last year in a [blog post](https://www.endpoint.com/blog/2018/07/09/training-tesseract-models-from-scratch) by Kamil.

AOCP will rapidly expand prior work and will help establish a digital pipeline for digitizing texts and creating a set of tools for students and scholars of historic texts. 

End Point is really excited to be a part of such a cool integration of technology and the humanities! 

Read more at:

- [https://www.openiti.org/projects/openitiaocp](https://www.openiti.org/projects/openitiaocp)
- [https://medium.com/@openiti/openiti-aocp-9802865a6586](https://medium.com/@openiti/openiti-aocp-9802865a6586)
- [http://kitab-project.org/corpus/](http://kitab-project.org/corpus/)
