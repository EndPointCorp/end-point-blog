const hljs = require('../../../js/highlight.min.js');

const langs = hljs.getRegisteredLanguageAliases();

const aliases = new Array(
  ...new Set(
      Object.keys(langs).reduce((acc, cur) => {
        return [...acc, ...langs[cur]];
      }, [])
    )
  );

const fs = require('fs');

fs.writeFileSync('supported_languages.json', JSON.stringify(aliases));
