# Changes made to the original 'wordcloud2.js' file
- Set shrinkToFit as true (line 208) <br> __(This was done so that if a word frequency was scaled too far, it would not be omitted from the wordcloud, instead the wordcloud will shrink to include it)__
- Added comment about AMD module (line 1229)