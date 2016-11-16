
=== Stratified cross-validation ===
=== Summary ===

Correctly Classified Instances         248               81.8482 %
Incorrectly Classified Instances        55               18.1518 %
Kappa statistic                          0.633 
Mean absolute error                      0.1871
Root mean squared error                  0.4023
Relative absolute error                 37.7102 %
Root relative squared error             80.7762 %
Total Number of Instances              303     

=== Detailed Accuracy By Class ===

               TP Rate   FP Rate   Precision   Recall  F-Measure   ROC Area  Class
                 0.783     0.152      0.812     0.783     0.797      0.879    Sick
                 0.848     0.217      0.824     0.848     0.836      0.879    Healthy
Weighted Avg.    0.818     0.187      0.818     0.818     0.818      0.879

=== Confusion Matrix ===

   a   b   <-- classified as
 108  30 |   a = Sick
  25 140 |   b = Healthy

==========================================================================================
XMeans
======
Requested iterations            : 1
Iterations performed            : 1
Splits prepared                 : 2
Splits performed                : 1
Cutoff factor                   : 0.5
Percentage of splits accepted 
by cutoff factor                : 0 %
------
Cutoff factor                   : 0.5
------

Cluster centers                 : 3 centers

Cluster 0
            45.94736842105263 8029.368421052632 30031.842105263157 85.73684210526316 13.657894736842104 44.8421052631579 354.7368421052632
Cluster 1
            148.35333333333332 1872.6666666666667 8291.08 13.266666666666667 2.953333333333333 13.813333333333333 54.89333333333333
Cluster 2
            885.7142857142857 637.7142857142857 3834.4761904761904 0.9523809523809523 0.9523809523809523 2.0 17.19047619047619

Distortion: 52.578638
BIC-Value : 676.233187


Time taken to build model (full training data) : 0.01 seconds

=== Model and evaluation on training set ===

Clustered Instances

0       36 ( 17%)
1      152 ( 73%)
2       21 ( 10%)
