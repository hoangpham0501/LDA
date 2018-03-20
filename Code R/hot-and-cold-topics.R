load("D:\\Visualize Data\\Code R\\model-lda-gibbs-300topics.RData")
load("D:\\Visualize Data\\Code R\\tm-corpus-pnas-abstracts.rda")
years <- levels(factor(abstracts$dmeta$year))
topics_n <- model_lda@k
theta <- posterior(model_lda)$topics

print(length(theta))
print(length(abstracts$dmeta$year))

theta_mean_by_year_by <- by(theta, abstracts$dmeta$year, colMeans)
theta_mean_by_year <- do.call("rbind",theta_mean_by_year_by)
colnames(theta_mean_by_year) = paste(1:topics_n)
theta_mean_by_year_ts <- ts(theta_mean_by_year, start = as.integer(years[1]))
theta_mean_by_year_time <- time(theta_mean_by_year)


theta_mean_lm <- apply(theta_mean_by_year, 2, function(x) lm(x ~ theta_mean_by_year_time))
theta_mean_lm_coef <- lapply(theta_mean_lm, function(x) coef(summary(x)))

theta_mean_lm_coef_sign <- sapply(theta_mean_lm_coef, '[',"theta_mean_by_year_time", "Pr(>|t|)")
theta_mean_lm_coef_slope <- sapply(theta_mean_lm_coef,'[',"theta_mean_by_year_time", "Estimate")


# Divide the trend slopes into positive and negative slopes
theta_mean_lm_coef_slope_pos <- theta_mean_lm_coef_slope[theta_mean_lm_coef_slope >= 0]

theta_mean_lm_coef_slope_neg <- theta_mean_lm_coef_slope[theta_mean_lm_coef_slope < 0]

p_level <- c(0.05, 0.01, 0.001, 0.0001)
significance_total <- sapply(p_level,
                             function(x) (theta_mean_lm_coef_slope[theta_mean_lm_coef_slope < x]))
#print(significance_total)
significance_neg <- sapply(1:length(p_level),
                           function(x) intersect(names(theta_mean_lm_coef_slope_neg),
                                                 names(significance_total[[x]])))
significance_pos <- sapply(1:length(p_level),
                           function(x) intersect(names(theta_mean_lm_coef_slope_pos),
                                                 names(significance_total[[x]])))

topics_hot <- as.numeric(names(sort(theta_mean_lm_coef_slope[significance_pos[[4]]], decreasing = TRUE)))
topics_cold <- as.numeric(names(sort(theta_mean_lm_coef_slope[significance_neg[,4]], decreasing = FALSE)))