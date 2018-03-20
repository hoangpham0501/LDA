library("tm")

load("D:\\Visualize Data\\Code R\\tm-corpus-pnas-abstracts.rda")

#heading_prepend <- function(x) PlainTextDocument(
  #paste(meta(x, tag = "heading"), x, sep = ""), origin = meta(x, tag="origin"),
  #id = meta(x, tag="id"), language = meta(x, tag="language"))


abstracts_corpus <- tm_map(abstracts, content_transformer(tolower))
# Remove special character and icon
abstracts_corpus <- sapply(abstracts_corpus, function(row) iconv(row, "UTF-8", sub="byte"))
# convert into corpus object
abstracts_corpus <- Corpus(VectorSource(abstracts_corpus))

# Convert into document-term matrix
dtm <- DocumentTermMatrix(abstracts_corpus, control = list(tolower = TRUE,
                                                           removePunctuation = TRUE,
                                                           removeNumbers= TRUE,
                                                           stemming = FALSE,
                                                           stopwords = TRUE,
                                                           minWordLength = 2))
dtm <- dtm[ , which(table(dtm$j) >= 1)]
save(dtm, file = "abstracts-dtm.RData")