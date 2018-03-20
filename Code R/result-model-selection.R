load("modelselection-result.RData")

library("latice")
print(xyplot(logLikelihood= topics, data = result,
             type= c("p", "a", "g"), fun = mean,
             ylab= "Log-likelihood", xlab = "Topics",
             scales = list(x=list(relation="free", at =
                                    c(50,100.200,300,400,500,600,1000)))))