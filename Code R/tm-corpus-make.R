meta_df <- read.table("D:\\Visualize Data\\meta.csv", fill = TRUE, header = TRUE, sep=",", 
                         quote ="\"", comment.char = "", encoding = "UTF-8", stringsAsFactors = F)
require ("tm")

abstracts_reader <- FunctionGenerator(function(...)
  function(elem, language, id){
    PlainTextDocument(x = elem$content,
                      datetimestamp = as.POSIXlt(Sys.time(), tz = "GMT"),
                      id = id,
                      origin = elem$uri,
                      language = language)})

abstracts_source <- DirSource(directory = "D:\\Visualize Data",
                                 pattern = "\\.abstract\\.txt", recursive = TRUE)

abstracts <- Corpus(abstracts_source, readerControl = list(reader = abstracts_reader, language = "english", encoding = "UTF-8"))

#Reformat abstract local paths
meta_df$abstract_local_path <- paste("./", meta_df$abstract_local_path, sep="")

# now metadata can be merged into corpus
for(name in names(meta_df)[-c(10 ,13 ,14 ,15 ,25)])
  meta(abstracts , tag = name) <- meta_df[name]

save(abstracts , file = "D:\\Visualize Data\\Code R\\tm-corpus-pnas-abstracts.rda", compress = TRUE)