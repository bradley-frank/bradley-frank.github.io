---
title: "Tips for the AST2003H/2017 Radio Astronomy Project"
excerpts: "The main aim of this project is design a good radio interferometer, within a set of
constraints."
tags:
    - post
    - teaching
    - astronomy
    - radio astronomy
last_modified_at: 2017-10-26T10:18:00
---

# Aims of the Project

The AST2003H/2017 Radio Astronomy Project (RAP) is meant to develop a variety of important
scientific and analytical skills. The main purpose of the project is to design a **good** radio
interferometer, within a set of operational constraints. The optimization problem is largely a
_secondary_ consideration -- in that you need to have a design process first _before_ you can start
optimizing, i.e., you need to have something to optimize!

The project is first and foremost a **astronomical** project.

Therefore, the **main** skills that each member of the project ought to develop are as follows:
* **Design** a reasonable mock/model image. 
* **Generate** a sensible array design.
* Use the mock image, the array design and the observational parameters to **simulate** a radio
  interferometric observation. 
* **Image** the the visibility data set to produce an output image. This needs to be compared with your
  input image to assess the performance of your telescope. 

You can start the optimizing once you have an idea of the design process, and after you've developed a
suitable understanding or intuition of what goes into the design into a _good_ array.

## Optimisation

There are several constraints that need to considered when designing your array. You have to balance
the cost of construction and operation; system temperature, efficiency, number of dishes and,
importantly, imaging performance. 

Optimisation is a tricky business, and your final design will be the best possible compromise of all
these factors. I imagine that some teams will design arrays that are under budget, but not sensitive
enough; other teams may design arrays that are insanely sensitive but cost too much to operate. Each
team needs to motivate what makes their design _optimal_. Each array won't be perfect, but the
**main** objective is to produce an array that generates good images.

## The Visibility Domain

It is essential that you appreciate the contents of [Chapter 3: Essential Radio Astronomy][era3]. In
particular, consider Section 3.3. Measurements of an astronomical source are made in the aperture
domain of a telescope, which have associated coordinates $$(u,v)$$. This is independent of the
wavelength at which you are observing, i.e., this is the same for an optical _and_ a radio
telescope. 

The domain described by the coordinates $$(u,v)$$ is referred as the _visibility_ domain, and the
measurements $$g(u,v)$$ are referred to as the visibilities. This is what's contained in the
measurement set produced by radio telescopes.

Any astronomical source has a representation in this aperture domain, which we can denote as
$$V(u,v)$$. The quantity that you measure on the _sky_ can be denoted in sky coordinates $$(l,m)$$
as follows: 

$$f(l,m) = \int_{-\infty}^{-\infty} \int_{-\infty}^{-\infty} g(u,v)e^{-2\pi i(ul + vm)}du dv$$

In practice, $$g'(u,v)=S(u,v)\times g(u,v)$$ is measured, where $$S(u,v)$$ is the sampling function
produced by your aperture, and referred to as a _convolution_. In our case, $$S(u,v)$$ is produced
by the radio telescope, and the equation described above is a Fourier Transform. 

Each pair of antennas (or baselines) produces a $$(u,v)$$ point at each instant in time, for each
channel or frequency increment. 

Thus, the job of the radio astronomer is to produce a reliable reconstruction of $$f(l,m)$$, and
this is a central consideration of your project -- you need a well sampled visibility domain to help
you _undo_ the convolution of the visibilities with your sampling function.

Usually, this is a one-sided process, i.e., you cannot change the array layout you have, you can
only work on the process of _deconvolution_ or imaging. For your project, you will be designing an
array that provides an optimal sampling in the $$(u,v)$$ domain, which will diminish the difficulty
with deconvolution.

## Making a Mock Image

You need to construct a mock image to use for your simulation, and this is done by inserting a
series of 2D Gaussian sources into an image. In your `dummy-settings.txt` file, you will find the
following section:

```
[sources]
source1=10h00m00.00s,-30d00m00.0s,1,3.0,1.0,90
source2=10h00m00.00s,-30d00m03.0s,1,1.0,1.0,90
source3=10h00m00.00s,-30d05m03.0s,1,10.0,1.0,45
```

Each line describes the distribution of the source, and the format is as follows:

```
<name>=<ra>,<dec>,<flux>,<gmaj>,<gmin>,gpa
```

where:
* The RA is in the format `12h34m56.78s`.
* The Dec is in the format `-12d34m56.78s`.
* The flux is in `Jy`.
* The major and minor axes of the 2D Gaussian, `gmaj` and `gmin`, respectively, are in arcseconds.
* The position angle `gpa` or orientation of the 2D Gaussian is in degrees.

Your sources ought to be distributed throughout the main beam of your telescope, and you can use any
of the formulae in the [ERA][era3] notes to calculate the field of view for your dishes. 

Also keep in mind that your highest resolution is determined by the largest baseline between dishes;
so this sets a natural limit on how close each source ought to be in the mock image. 

## Designing an array

I have provided a notebook that illustrates the MeerKAT design, but there are many different designs
to choose from. For example, the VLA is designed to reach a full synthesis after about 8-hours, and
the GMRT has a similar design. The WSRT telescope is an east-west array with redundant spacings,
which imprints the immediately recognisable PSF in the image. The MeerKAT and ASKAP arrays are
semi-random, which has the benefit of providing a continuous range of sensitivities as a function of
resolution. 

## Simulation
The CASA task [`simobserve`][simobserve] is quite a lovely and sophisticated task. For a given antenna
configuration and  mock image, [`simobserve`][simobserve] calculates the $$(u,v,w)$$ positions
corresponding to the observation; calculates the Fourier Transform $$g(u,v,w)$$ of your mock image
and _samples_ this distribution at the discrete $$(u,v,w)$$ coordinates corresponding to your
observation. 

The parameters of your mock observation are defined in your `dummy-settings` file as follows: 

```
[observation]
ra = 10h00m00.0s
dec = -30d00m00.0s
filename = Gaussians
imsize = 1024
pixelsize = 4.0arcsec
reffreq = 1420MHz
freqint = 1GHz
integration = 10
totaltime = 7200s
project = sim
skymodel = Gaussians.im
config = brads-random-array.cfg
```

This observation section is used by both the `make-model.py` and the `make-sim.py` scripts. In this
case, the `ra` and `dec` fields denote the centre of your simulated observation. The `ra` and `dec`
values are used to calculate a pointing file, which is used by [`simobserve`][simobserve]. The
`filename` field denotes the leading name of your mock image. 

Now, your mock image file is pixelated, and you need to define how large the image is, in pixels,
and how large each pixel is. 
For a given field of view, $$N_\mathrm{pixels}\times\theta_{pixel}\sim\theta_\mathrm{FoV}$$. 

Now the frequency interval here is `1GHz`. Don't forget to **change this**! Also, the default
integration time is `10` seconds. Both these values need to be changed, i.e., the frequency
interval for this project is `10MHz`, but the integration time depends on the longest baseline in
your array, that is, the longer the baseline the shorter your integration time ought to be!

Finally, you need to specify the project name, skymodel and the configuration. Output files will be
dumped into the `project/` directory after a successful simulation. Suppose you've used a
configuration called `brads-config.cfg`. The `project/` directory will thus contain the folling files:

```
project.brads-config.ms/        
project.brads-config.noisy.ms/  
project.brads-config.ptg.txt    
project.brads-config.simobserve.last                                    
project.brads-config.skymodel/                                          
project.brads-config.skymodel.flat/
```
You need to use the `project.brads-config.ms` file for your imaging, and you usually specify the
visibility as `vis=project.brads-config.ms`.

## Imaging aka Deconvolution aka Cleaning

Deconvolution is the process of iterative image reconstruction; it is the iterative removal of the
effect of the telescope's sampling function. CASA uses the `CLEAN` task to do this, and you can
run the task using the script `make-image.py`. There is a very useful presentation on the details of
`CLEAN`[clean], which will be very interesting as a reference.

The script `make-image.py` makes use of the settings file, and the parameters are defined in the
associated section:

```
[clean]
vis = sim/sim.brads-random-array.ms
imagename          =  sim.dirty
mode               =  mfs
niter              =  100
threshold          =  0.0mJy
psfmode            =  clark
imagermode         =  csclean
ftmachine          =  mosaic
imsize             =  1024
cell               =  4arcsec
stokes             =  I
weighting          =  natural
robust             =  0.0
```

I have included the important parameters here. The `mode='mfs'` chooses the _multi-frequency
synthesis_ algorithm, which is a redundant since we are only imaging a single frequency. `niter=100`
instructs the algorithm to perform 100 `CLEAN` iterations; please consult the associated
[documentation][clean] for more details on how this works. The `threshold='0.0mJy'` parameter controls
when the algorithm stops; in this case, the algorithm will stop when/if the brightest remaining
pixel is equal to `0.0mJy`. 

The `threshold` and `niter` parameters are closely related; the algorithm will stop when either
condition is reached. 

Finally, the `cell` parameter sets the pixel size, and the `imsize` parameter defines the size of
the image in pixels. It is common practice to define the `imsize` parameter in powers of 2, since
this makes FFT's easier to grid. 

In the case above, I have misleadingly provided the output naming tag of `sim.dirty`; since `n=100`,
the output image will _not_ be the dirty image. 

After the `CLEAN` algorithm has completed, the following files will be produced:

```
sim.dirty.flux/                                                                                             
sim.dirty.image/                                                                                            
sim.dirty.image.fits                                                                                        
sim.dirty.model/                                                                                            
sim.dirty.psf/                                                                                              
sim.dirty.psf.fits                                                                                          
sim.dirty.residual/
```

The files contain the following:
* `*.flux`: This contains the estimate of the primary beam of the telescope. The FWHM of this image
  will be a close match of the calculated FWHM corresponding to your dish size. 
* `*.image`: This contains the output image. The `fits` associated image has been generated for your
  convenience.
* `*.model`: This contains the pixels used when doing the deconvolution, and will generally cluster
  around the positions of your mock sources. If you've computed the dirty image, the `*.model` image
  will be empty. 
* `*.psf`: This is the Fourier Transform of the telescopes sampling function. The `fits` image has
  been generated using `exportfits`, and is easily imported into a notebook using the _APLPY_
  software.
* `*.residual`: This is the residual after the bright sources have been deconvolved. 

### The Dirty Image
Setting `niter=0` simply instructs the `CLEAN` algorithm to do a Fourier Transform of the visibility
data, without performing _any_ deconvolution. The dirty image is the inverse Fourier Transform of
a convolution between the source visibility function and the sampling function produced by the
telescope configuration. An ideal dirty image has a minimal amount of coherent structure imprinted
from the sampling function. 

### The CLEAN Image
Setting `niter>0` instructs the `CLEAN` algorithm to deconvole the PSF. 

### Weighting the Visibilities
You can control the shape and structure of the deconvolved beam by weighting the visibilities, using
the `weighting` and the `robust` parameter. Setting `weighting='briggs'` allows you to _tune_ the
PSF by choosing different values of the robust parameter. With `weighting='briggs'` you can vary the
`robust` parameter between -2.0 and +2.0. In short, `weighting='briggs'; robust=2` maximizes
sensitivity, while `weighting='briggs'; robust=-2` maximizes the resolution.

## Conclusion

The concepts of simulation and imaging are fairly straightforward, but the implementation can be
tricky. Therefore, it is very important for you to try to run the simulations yourself. Start off
with a few sources and a small number of dishes; make dirty images, or clean _lightly_, i.e., with a
small value of `niter`. Soon you will develop an intuition for the process and, importantly, an
understanding of how to design your optimal array. Good luck!


[era3]: http://www.cv.nrao.edu/~sransom/web/Ch3.html
[simobserve]: https://casa.nrao.edu/docs/taskref/simobserve-task.html
[clean]: https://science.nrao.edu/opportunities/courses/casa-caltech-winter2012/Carpenter_Radio_Imaging_and_Clean_Caltech2012.pdf
