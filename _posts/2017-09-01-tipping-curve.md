---
title: "Worksheet 2: The Tipping Curve"
excerpt: "In this notebook, I will illustrate how you can generate a window function, and how you
can calculate the associated Fourier Transform"
tags: 
  - post
  - teaching 
  - astronomy
  - cloud
last_modified_at: 2017-09-01T14:00:00
---

# Worksheet 2: The Tipping Curve

Please refer to [Chapter 2 of the ERA Notes][era-ch2]. 

Recall that if the zenith opacity is sufficiently small, we can write the system temperature of a telescope as follows:

$$ T_\mathrm{sys} = (T_\mathrm{r} + T_\mathrm{cmb})+T_\mathrm{b} $$

where $$T_\mathrm{b}$$, the equivalent temperature of the atmosphere, is given by $$T_b=T_{atm} \tau_z \sec z$$.

Since $$T_r$$ and $$T_{cmb}$$ are constants, we can thus write down the following expression for the **tipping curve**:

$$\tau_z \approx \frac{\Delta T_{sys} / T_{atm}}{\Delta \sec z}$$

# Questions

1. For each data set (measurement), use the data provided to estimate the system temperature _and_ calculate the temperature of the CMB.
2. For each measurement, calculate the RMS deviation of the receiver temperature $$T_\mathrm{r}$$. Now, plot the RMS deviations and the measured temperature and the calculated temperature $$T_\mathrm{cmb}$$. What can you conclude?

#### Tips & Assumptions
* You may assume that the ambient atmospheric temperature ahs been measured to be $$T_\mathrm{atm}=300K$$.
* I have used a simple python library to fit a straight line to the tipping curve. This is a generic library to fit polynomials to data, and there is an associated function to calculate the resulting coefficients. 
* The slope of the tipping curve is $$[T_\mathrm{r}+T_\mathrm{cmb}]/T_\mathrm{atm}$$, and the x-intercept is $$\sec(z)$$. Since the data is noisy, you can use a fit to estimate these parameters.
* The $$T_\mathrm{r}$$ receiver measurements resemble a Gaussian distribution. You can use this concept to estimate the mean value $$<T_\mathrm{r}>$$, and the RMS deviation of the measurements.

## Loading and Plotting the Data

The tipping curves are all located in the directory `/data/ast2003h/`, but you can also view and
download them here.

You will find the following files in the `/data/ast2003h/` directory:

* [tipping-curve-1.txt][tc1]
* [tipping-curve-2.txt][tc2]
* [tipping-curve-3.txt][tc2]
* [tipping-curve-4.txt][tc3]
* [tipping-curve-5.txt][tc4]
* [tipping-curve-example.txt][tcex]

In each file, column-1 corresponds to $$\sec(z)$$, column-2 corresponds to $$T_\mathrm{sys}/T_\mathrm{atm}$$ and column-3 corresponds to measurements of $$T_\mathrm{r}$$.

**Note**: In `tipping-curve-example.txt` there is an extra column-4, which corresponds to a _fit_ to the tipping curve data. This is **not** present in the other files.

In the cells below I illustrate how to extract the data from `tipping-curve-example.txt`, and I plot the relevant data in two subplots. I've also plotted the best fit curve that I calculated previously. 


```python
import numpy as np
import pylab as pl
%matplotlib inline
```


```python
data = pl.loadtxt('/data/ast2003h/tipping-curve-example.txt')
secz = data[:,0]
tsys_over_tatm = data[:,1]
trx = data[:,2]
fit = data[:,3]
```


```python
pl.figure(figsize=(10,5))
pl.subplot(121)
pl.plot(secz, tsys_over_tatm, 'ko', label='data')
pl.plot(secz, fit, 'r-', lw=5, label='best fit')
# This sets up the x/y limits, axis labels and plot title.
pl.xlim(0,10)
pl.ylim(0,0.3)
pl.xlabel('$\sec(z)$', fontsize=16)
pl.ylabel('$T_\mathrm{sys}/T_\mathrm{atm}$', fontsize=16)
pl.legend(loc=4, numpoints=1)
pl.title('Tipping Curve', fontsize=20)

pl.subplot(122)
pl.hist(trx)
pl.xlabel('$T_\mathrm{r}$', fontsize=14)
pl.ylabel('Number of Measurements', fontsize=14)
pl.title('Receiver Temperature \n Measurements', fontsize=20)
```
![tipping-curve]({{site.url}}/assets/images/tipping-curve-worksheet_4_1.png)

### Submitting your worksheet.

You can simply copy-and-paste these commands into your own Jupyter Notebook; the commands ought to
work sensibly. 

When you're done, _download_ the notebook and _upload_ it on the Vula website.

[era-ch2]: http://www.cv.nrao.edu/~sransom/web/Ch2.html
[tc1]: /assets/data/tipping-curve-1.txt
[tc2]: /assets/data/tipping-curve-2.txt
[tc3]: /assets/data/tipping-curve-3.txt
[tc4]: /assets/data/tipping-curve-4.txt
[tc5]: /assets/data/tipping-curve-5.txt
[tcex]: /assets/data/tipping-curve-example.txt
