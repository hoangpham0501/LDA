library("topicmodels")
getSlots("LDA_Gibbs")


# ldaGibbsSamples() is needed for the repeated call of the LDA model estimation in order
# to produce a chain of model samples.

ldaGibbsSamples <- function(dtm, k, burniniter, sampleinterval, nsamples, control = NULL, model = NULL,...){
  #Vaue: return a list of objects of class "LDA"
  #Note: the "call" slot of samples contains just the wrapper's variable names, is therefore useless

  
  #check control and remove iter parameter, if present:
  if(!is.null(control)){
    stopifnot(is.list(control))
    control <- control[names(control) != "iter"]
  }
  chain <- list(LDA(dtm, k, method = "Gibbs", c(control, list(iter= burniniter), model,...)))
  for(jj in 1:nsamples){
    lastSampleIndex <- jj-1
    if(jj == 1) lastSampleIndex <- 1
    
    chain[[jj]] <- LDA(dtm, k, method="Gibbs", c(control, list(iter=sampleinterval)), model=chain[[lastSampleIndex]], ... )
  }
  return(chain)
}

#logPwzt() calculates the log-likelihood p(w|z,K) of one model sample.

logPwzT <- function(model){
  BETA <- model@delta
  M <- model@Dim[1] #Number of document
  V <- model@Dim[2] #Number of unique terms...W, or V
  K <- model@k      #Number of topics (T)
  
  nwsum <- rowSums(model@nw)
  lPwz1 <- K*(lgamma(V*BETA) - V * lgamma(BETA))
  
  #second factor
  lPwz2 <- 0
  for(j in 1:K){
    subsum <- 0
    for(w in 1:V) subsum <- subsum + lgamma(model@nw[j,w]+ BETA)
    lPwz2 <- lPwz2 + (subsum = lgamma(nwsum[j] + V*BETA))
  }
  
  lPwz <- lPwz1 + lPwz2
}

harmonicMeanPwT <- function(chain, precision = 2000L){
  library("Rmpfr")
  
  logLikelihoods <- sapply(chain, logPwzT)
  
  llMed <- median(logLikelihoods)
  as.double(llMed - log(mean(exp(-mpfr(logLikelihoods, prec = precision) + llMed))))
}
