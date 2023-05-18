# Machine Learning

Since this is a Cloud Computing Course, it will focus more on deploy Machine Learning Application efficiently on the cloud.

#### Why Distributed Training?
- Using the right hardware condiguration can dramatically reduce training time
- And a shorter training time makes for **faster iteration** to reach your modeling goals

Training models is slow

<img src="images/1.png" width="500"/>

Too many computations

<img src="images/2.png" width="500"/>

### Data Parallelism

<img src="images/3.png" width="500"/>

<img src="images/4.png" width="500"/>

<img src="images/6.png" width="500"/>

<img src="images/8.png" width="500"/>

#### All Reduce

<img src="images/9.png" width="500"/>

<img src="images/10.png" width="500"/>

<img src="images/11.png" width="500"/>

##### Issue 
  
  - Master is the bottleneck for scaling up
  - Most of the bandwidth and computation go to Master, while Workers not doing things

<img src="images/12.png" width="500"/>

(P - 1) * N is all parameters in the cluster
(P - 1) * N / p is the amount of parameters that each machine deals with

<img src="images/13.png" width="500"/>

<img src="images/14.png" width="500"/>


##### Description

- Each machine send a parameter to other machine
- Each machine receive required parameters for one sum
- Each machine do sum up, and share the result to each other

### Model Parallelism

Works best for models that each individual part can be computed at parallel. In the following example, as GPU0 finishes mat mul, it can pass to GPU 1 and GPU1 can work on add. Don't have to wait all works of mat mul to finish before doing add.

Sometimes, we use a combination of data parallelism, and model parallelism.

<img src="images/5.png" width="500"/>