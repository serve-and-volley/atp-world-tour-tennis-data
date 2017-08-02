require(scatterplot3d)

data <- read.csv(file="Desktop/R-project/aces_height_weight_2016.csv", head=TRUE, sep=",")

serve_pts_per_ace = data$serve_pts_per_ace
height = data$height
weight = data$weight

s3d <- scatterplot3d(height, weight, serve_pts_per_ace, color = "blue", pch = 4, angle = 45)

lm(serve_pts_per_ace ~ height + weight)
reg3 = lm(serve_pts_per_ace ~ height + weight)
s3d$plane3d(reg3)
