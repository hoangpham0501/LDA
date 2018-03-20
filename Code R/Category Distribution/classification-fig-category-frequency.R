library(lattice)

theme.nopadding <- list(layout.heights = list(top.padding = 0, 
                                              main.key.padding = 0,
                                              key.axis.padding = 0,
                                              axis.xlab.padding = 0,
                                              key.sub.padding = 0,
                                              bottom.padding = 0) ,
                        layout.widths = list(left.padding = 0,
                                             key.ylab.padding = 0,
                                             ylab.axis.padding = 0,
                                             axis.key.padding = 0,
                                             right.padding = 0))

categories_table <- table(categories_2016$pretty)
categories_table_barchart <- rev(categories_table[category_levels$pretty])

print(barchart(categories_table_barchart, xlab = NULL,
               par.settings = theme.nopadding, panel = function(...){
                 args <- list(...); panel.barchart(... , col = rev(category_levels$color));
                 panel.text(args$x+10 , args$y, args$x, fontsize = 10)
                 }))