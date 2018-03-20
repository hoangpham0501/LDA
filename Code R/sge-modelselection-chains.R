library ("topicmodels")

load("C:\\CollectingData\\Code R\\abstracts-dtm.RData")
source("C:\\CollectingData\\Code R\\lda-gibbs-tools.R")

chains <- c(8, 8, 8, 8, 8, 8, 8, 6)
parameters <- list(chains = chains,
                    seeds = 1:sum(chains),
                    topics = rep(c(50 , 100 , 200 , 300 , 400 , 500 , 600 , 1000) ,chains),
                    topicsChainId = unlist(sapply(chains , function(x) seq(1,x))),
                    samples = rep(c(10 , 10, 10, 10, 10, 10, 10, 2) , chains),
                    burnIn = rep(c(1100 , 1100 , 1100 , 1100 , 1100 , 1100 , 1100 , 800) , chains),
                    sampleInterval = rep(c(100 , 100 , 100 , 100 , 100 , 100 , 100 , 100) , chains))
jobid <- as.numeric(Sys.getenv("SGE_TASK_ID"))
print(jobid)

chain <- ldaGibbsSamples(dtm,
                         k = parameters$topics[jobid],
                         burniniter = parameters$burnIn[jobid],
                         sampleinterval = parameters$sampleInterval[jobid],
                         nsamples = parameters$samples[jobid],
                         control = list(alpha = 50/parameters$topics[jobid], seed = parameters$seeds[jobid]))

# concatenate filename , save file :
FILE <- paste("modelselection-chain-", jobid , "-", parameters$topics[jobid ], ".Rda", sep = "")
save(chain , file = FILE)

save(parameters , file = "modelselection-parameters.Rda")