# Two-Photons-Entanglement Reference

# Summary of PhysRevA.105.063706 and Key Considerations for Numerical Simulation

This paper (PhysRevA.105.063706) mainly investigates how methods such as **multiplexing** and **cavity modulation** can be used to eliminate frequency-domain entanglement in **cascaded biphotons**, thereby generating high-quality single-photon sources with high **purity** and **indistinguishability**.

The following is a summary of the main points of the paper, along with important considerations for implementing numerical simulations.

## I. Summary of the Main Points

### 1. Core Objective

* In quantum communication and quantum computing, single-photon sources with **high indistinguishability** and **high purity** are required.

* Cascaded biphotons (**Signal** and **Idler** photons) generated through **four-wave mixing (FWM)** typically exhibit strong frequency anti-correlation (**anti-correlation/frequency entanglement**). The goal of this paper is to **eliminate this frequency entanglement and reduce the entanglement entropy $S$ to a very low value**.

### 2. Two Methods for Eliminating Frequency Entanglement

#### Method 1: Multiplexed Atomic Ensembles + Cavity Modulation + Phase Compensation (Main Approach)

* **Mechanism:**
  The Idler or Signal photon is allowed to pass through a two-mirror optical cavity with one highly reflective mirror, combined with a relative phase shift, such as $\phi=\pi$, which produces destructive interference.

* **Effect:**
  Through destructive interference produced by the optical cavity and phase modulation, the frequency anti-correlated distribution is suppressed, effectively shaping/compressing the frequency spectrum into a symmetric and narrow distribution.

* **Results:**
  When 4 atomic ensembles (AEs) are multiplexed, the frequency entanglement entropy can be reduced to approximately $S \approx 0.006$, while the single-photon purity reaches **0.999**. When the number of AEs is increased to 64, the purity can exceed **0.9995**.

  This method **does not sacrifice the photon generation rate in the same way as conventional frequency filtering (truncation)**.

#### Method 2: Symmetric Pumping + Non-Discriminating Detection (Symmetrization Approach)

* **Mechanism:**
  The pumping directions of the two atomic ensembles are reversed so that the detectors cannot distinguish between the Signal and Idler photons. This is achieved using non-discriminating detectors $D_1$ and $D_2$.

* **Result:**
  The spectral function is forced to become symmetric, reducing the entanglement entropy to approximately $S \sim 0.3$ and achieving a single-photon purity of approximately **0.9226**.

  The architecture is simpler, but its performance is somewhat inferior to Method 1.

## II. Important Considerations for Numerical Simulation

If you are writing a program, such as Python, MATLAB, or Julia, to simulate the biphoton spectral function, **Schmidt decomposition**, and entanglement entropy presented in this paper, pay particular attention to the following key steps and numerical details.

### 1. Biphoton Spectral Function Setup

The original biphoton spectral function $f(\omega_s,\omega_i)$ is defined as

$$
f(\omega_s,\omega_i)
=
\frac{
e^{-(\Delta\omega_s+\Delta\omega_i)^2\tau^2/8}
}{
\frac{\Gamma_3^N}{2}-i\Delta\omega_i
}
$$

#### Simulation Considerations

* **Dimensionless Units:**
  The frequency-related variables in the paper, including $\Delta\omega_s$, $\Delta\omega_i$, $\Gamma_c$, and $\Gamma_3^N$, are normalized using the natural decay rate of a single atom, $\Gamma$, as the reference unit.

* **Typical Parameter Values:**
  The parameters used in the paper can be adopted for the simulation, such as the superradiant decay rate

  $$
  \frac{\Gamma_3^N}{\Gamma}=5
  $$

  and the pulse duration

  $$
  \Gamma\tau=0.25
  $$

### 2. Cavity Transfer Function

The lossless transfer function of a single-sided cavity is

$$
C_t(\Delta\omega,\Gamma_c)
=
\frac{
\Gamma_c+i2\Delta\omega
}{
\Gamma_c-i2\Delta\omega
}
$$

#### Simulation Considerations

* **Sign Convention and Complex Arithmetic:**
  Carefully verify the signs of the imaginary terms. In the paper, the imaginary part in the numerator is $+i2\Delta\omega$, while the denominator contains $-i2\Delta\omega$.

* When combining multiple AEs, the addition and subtraction of complex phases, such as

  $$
  e^{i\pi}=-1
  $$

  are crucial for producing destructive interference.

  Therefore, when implementing the simulation, make sure that the arrays are explicitly stored as **complex-valued arrays**.

### 3. Discretization Grid and Frequency Cutoff

#### Frequency Range

* When calculating the entanglement entropy, the sampling range must be sufficiently large to include both the main spectral peak and its decaying tails.

* In the paper, the frequency range used for calculating $S$ is

  $$
  \pm150\Gamma
  $$

#### Resolution / Grid Size

* The frequency grids for $\Delta\omega_s$ and $\Delta\omega_i$ must be constructed as two-dimensional matrices with dimensions

  $$
  N\times N
  $$

* **Important:**
  When the cavity linewidth $\Gamma_c$ becomes very small, for example

  $$
  \frac{\Gamma_c}{\Gamma}\rightarrow0
  $$

  the spectrum becomes extremely narrow, resembling a Lorentzian or a very thin spectral line.

  If the frequency grid does not have sufficient resolution, the extremely narrow full width at half maximum (FWHM) cannot be properly resolved. This can lead to **numerical instability in the integration or incorrect Schmidt eigenvalues**.

  Therefore, sufficiently fine sampling should be used around the central frequency region.

### 4. Singular Value Decomposition / Matrix Diagonalization (Schmidt Decomposition)

The paper uses Schmidt decomposition to calculate the entanglement entropy $S$ and the single-photon purity $\mathrm{Tr}(\rho_i^2)$.

#### Step 1: Construct the 2D Spectral Matrix

Construct the spectral matrix

$$
F_{j,k}
=
f_{\mathrm{MP}}(\omega_{s,j},\omega_{i,k})
$$

where $f_{\mathrm{MP}}$ denotes the multiplexed biphoton spectral function.

#### Step 2: Calculate the Single-Photon Spectral Correlation Kernel

The correlation kernel is

$$
K_1(\omega,\omega')
=
\int
f_{\mathrm{MP}}(\omega,\omega_1)
f_{\mathrm{MP}}^*(\omega',\omega_1)
\,d\omega_1
$$

In numerical calculations, this corresponds approximately to the matrix multiplication

$$
K_1
=
F F^\dagger\,d\omega_i
$$

where $F^\dagger$ denotes the conjugate transpose of $F$.

#### Step 3: Diagonalize the Kernel or Perform SVD

Diagonalize $K_1$ to obtain its eigenvalues $\lambda_n$.

Alternatively, directly perform **singular value decomposition (SVD)** on the normalized spectral matrix $F$.

If

$$
F=U\Sigma V^\dagger
$$

then the squared singular values

$$
\sigma_n^2
$$

correspond to the Schmidt probabilities

$$
\lambda_n.
$$

#### Numerical Details

* **Normalization:**
  Make sure that all Schmidt probabilities are normalized such that

  $$
  \sum_n\lambda_n=1
  $$

* **Entanglement Entropy:**

  $$
  S
  =
  -\sum_n\lambda_n\log_2(\lambda_n)
  $$

  In numerical calculations, when $\lambda_n\rightarrow0$, evaluating $\log_2(0)$ produces numerical errors such as `NaN` or `Inf`.

  Therefore, a small cutoff should be applied. For example, only include terms satisfying

  $$
  \lambda_n>10^{-12}
  $$

  in the entropy calculation.

* **Purity:**

  $$
  \mathrm{Purity}
  =
  \sum_n\lambda_n^2
  $$

  Equivalently, for the reduced density matrix,

  $$
  \mathrm{Purity}
  =
  \mathrm{Tr}(\rho_i^2).
  $$

### 5. Recursive Relationship for the Number of Ensembles

When simulating 4, 8, or even 64 AEs, as in Eqs. (18)--(20):

* The program can use a recursive structure or a loop to progressively construct the **effective spectral function**.

* Pay particular attention to the alternating introduction of the phase factor

  $$
  e^{i\pi}
  $$

  during each multiplexing step, since the relative phase is essential for producing the desired destructive interference.
