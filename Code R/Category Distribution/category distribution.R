load("D:\\Visualize Data\\Code R\\tm-corpus-pnas-abstracts.rda")

categories_2016_major <- abstracts$dmeta$category[abstracts$dmeta$year == 2016]
categories_2016_minor <- abstracts$dmeta$category_merged[abstracts$dmeta$year == 2016]
# Create data frame
categories_2016 <- data.frame(major=categories_2016_major, minor = categories_2016_minor,
                              stringsAsFactors =  FALSE)
categories_2016$major_abbr <- factor(categories_2016_major)
print(levels(categories_2016$major_abbr))
# Match categories with their short names
levels(categories_2016$major_abbr) <- c("(BS)", "(HOSF)", "(KS)", "(MEF)", "(NMSF)", "(Per)", 
                                        "(PS)", "(SCCH)", "(SCDC)", "(SCIF)", "(SCLE)", "(SS)")

categories_2016$pretty <- paste(categories_2016$minor, categories_2016$major_abbr)

# differentiate major categories by color
category_levels <- unique(categories_2016)
category_levels <- category_levels[order(category_levels$major,
                                         category_levels$minor),]
rownames(category_levels) <- category_levels$pretty
category_levels$color <- factor(category_levels$major)
#Match color with the category_level
levels(category_levels$color) <- c("#00CC33", "#0033CC", "#CC0099", "#00EEFF", "#00EE00", "#0000FF",
                                   "#EE00FF", "#FFEE00", "#EE3300", "#9900CC", "#CC00CC", "#FF00FF")
category_levels$color <- paste(category_levels$color)