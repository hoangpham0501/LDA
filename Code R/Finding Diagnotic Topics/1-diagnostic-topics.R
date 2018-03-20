load("D:\\Visualize Data\\Code R\\model-lda-gibbs-300topics.RData")

# Extract theta for the year 2016 from the fitted model's topics posteriors
theta <- posterior(model_lda)$topics[abstracts$dmeta$year == 2016,]

# Taking the mean by categories
theta_mean_by <- by(theta, categories_2016$pretty, colMeans)
theta_mean <- do.call("rbind", theta_mean_by)

# With all theta available, select the most diagnotic topics of each of these categories
# Calculate mean ratio
theta_mean_ratios <- theta_mean
for (ii in 1:nrow(theta_mean)){
  for (jj in 1:ncol(theta_mean)) {
    theta_mean_ratios[ii,jj] <- theta_mean[ii, jj]/sum(theta_mean[ii, -jj])
    
  }
}
# Sort topics by ratio
topics_by_ratio <- apply(theta_mean_ratios, 1,
                         function(x) sort(x, decreasing = TRUE, index.return = TRUE)$ix)
topics_most_diagnostic <- topics_by_ratio[1,]

# reduce the mean theta matrix to just the most diagnostic topics per category
theta_diagnostic <- theta_mean_ratios[, topics_most_diagnostic]
colnames(theta_diagnostic) <- topics_most_diagnostic