library("topicmodels")
load("D:\\Visualize Data\\Code R\\abstracts-dtm.RData")
# returned after 2000 iterations of Gibbs sampling with K = 300 topics
# Dirichlet hyperparameters beta = 0.1 (topics) and anpha = 50/K (documents)

# Problem: There are some docs have no words (cause the condition of selecting dtm) 
# Solution: remove all docs without words and the abstract corpus respectively

#rowTotals <- apply(dtm , 1, sum) #Find the sum of words in each Document
#dtm.new   <- dtm[rowTotals> 0, ]           #remove all docs without words

#Find the abstract corpus respectively
#empty.rows <- dtm[rowTotals == 0, ]$dimnames[1][[1]]
#Remove abstract corpus
#abstracts <- abstracts[-as.numeric(empty.rows)]

system.time(model_lda <- LDA(dtm, 300, method="Gibbs", control= list(iter=2000, seed=33)))
save(model_lda, file="D:\\Visualize Data\\Code R\\model-lda-gibbs-300topics.RData")
#save(abstracts , file = "D:\\Visualize Data\\Code R\\tm-corpus-pnas-abstracts.rda", compress = TRUE)