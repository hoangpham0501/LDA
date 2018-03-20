library("topicmodels")
load("D:\\Visualize Data\\Code R\\abstracts-dtm.RData")
# returned after 2000 iterations of Gibbs sampling with K = 300 topics
# Dirichlet hyperparameters beta = 0.1 (topics) and anpha = 50/K (documents)

system.time(model_lda <- LDA(dtm, 300, method="Gibbs", control= list(iter=2000, seed=33)))
save(model_lda, file="model-lda-gibbs-300topics.RData")