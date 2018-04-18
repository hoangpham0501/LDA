library("tm")

load("D:\\Visualize Data\\Code R\\tm-corpus-pnas-abstracts.rda")

#heading_prepend <- function(x) PlainTextDocument(
  #paste(meta(x, tag = "heading"), x, sep = ""), origin = meta(x, tag="origin"),
  #id = meta(x, tag="id"), language = meta(x, tag="language"))

# Add stop word list
my_stopwords <- read.table("D:\\Visualize Data\\Code R\\stopwords-en.txt", sep=",",quote ="\"", 
                           comment.char = "", encoding = "UTF-8", stringsAsFactors = F)
adverbs <- read.table("D:\\Visualize Data\\Code R\\adverbs.txt", sep=",",quote ="\"", 
                      comment.char = "", encoding = "UTF-8", stringsAsFactors = F)

my_stopwords <- as.character(my_stopwords$V1)
adverbs <- as.character(adverbs$V1)
my_stopwords <- c(my_stopwords, adverbs)

#abstracts_trans <- tm_map(abstracts, content_transformer(tolower))

# Remove special character and icon
abstracts_rc <- sapply(abstracts, function(row) iconv(row, "UTF-8", sub="byte"))
#abstracts_rc <- sapply(abstracts, function(row) iconv(row, "WINDOWS-1252", "UTF-8"))
#abstracts_corpus <- tm_map(abstracts, content_transformer(function(x) iconv(enc2utf8(x), sub = "byte")))
# convert into corpus object
abstracts_corpus <- Corpus(VectorSource(abstracts_rc), readerControl = list(encoding = "UTF-8"))

# Convert into document-term matrix
dtm <- DocumentTermMatrix(abstracts_corpus, control = list(tolower = TRUE,
                                                           removePunctuation = TRUE,
                                                           removeNumbers= TRUE,
                                                           stemming = FALSE,
                                                           stopwords = my_stopwords,
                                                           wordLengths = c(2, Inf)))

# deleted any words that occurred in less than three abstracts
dtm <- dtm[ , which(table(dtm$j) >= 3)]
save(dtm, file = "D:\\Visualize Data\\Code R\\abstracts-dtm.RData")