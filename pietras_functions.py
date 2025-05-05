import numpy as np
import scipy.stats

def chisquared(observed, expected, df=1):
    """
    Computes the Chi-squared and p-value for set of observed and expected data sets.

    Parameters:
    observed (list): The observed frequencies from the data.
    expected (list): The expected frequencies under the null hypothesis.
    df (int, optional): Degrees of freedom, default is 1.

    Returns:
    tuple: (Chi-squared, p-value)
    """
    x2 = 0
    for i in range(len(observed)):
        x2 += ((observed[i] - expected[i]) ** 2) / expected[i]

    pval = 1.0 - scipy.stats.chi2.cdf(x2, len(observed) - 1)

    return x2, pval

def linear_least_squares(x, y):
    """
    Computes the linear least-squares regression line for a given set of data points (x, y).

    Parameters:
    x (numpy.ndarray): 1D array of input values.
    y (numpy.ndarray): 1D array of output values.

    Returns:
    tuple: (m, b, se_m, se_b) where:
        - m (float): Slope of the best-fit line.
        - b (float): Intercept of the best-fit line.
        - se_m (float): Standard error of the slope.
        - se_b (float): Standard error of the intercept.
    """

    x = np.array(x, dtype=np.float64) # ensure input is np arrays
    y = np.array(y, dtype=np.float64)

    X = np.vstack([x, np.ones_like(x)]).T # construct matrix [x, 1] for y = mx + b
    Y = y.reshape(-1, 1) # y is column vec

    XTX_inv = np.linalg.inv(np.dot(X.T, X))  # Beta = (X^T X)^(-1) X^T Y
    beta = np.dot(XTX_inv, np.dot(X.T, Y))
    m, b = beta.flatten() # get m and b

    y_fit = m * x + b
    residuals = y - y_fit # get residuals
    n = len(x)
    sigma_squared = np.sum(residuals**2) / (n - 2) # variance of residuals (2 params)

    cov = sigma_squared * XTX_inv # Covariance matrix
    se_m = np.sqrt(cov[0, 0])  # standard error of m and b (sqrt of diagonals)
    se_b = np.sqrt(cov[1, 1])

    return m, b, se_m, se_b

def compute_crosscor(fref, ftest, in_spectral = True):
    """
    Computes the cross correlation between fref and ftest.

    Parameters:
    fref (numpy.ndarray): The refrence function
    ftest (numpy.ndarray): The test function
    in_spectral (bool): Compute in spectral space (true), or physical (false). Default True

    Returns:
    crosscor: (numpy.ndarray): The cross correlation between fref and ftest.
    None: could not be computed due to mismatch in array length
    """

    fref = np.array(fref)
    ftest = np.array(ftest)

    if len(fref) != len(ftest):
        print(f"ERROR! FREF {len(fref)} AND FTEST {len(ftest)} MUST BE THE SAME LENGTH!")
        return

    if in_spectral:
        return np.fft.ifft(np.fft.fft(fref) * np.conj(np.fft.fft(ftest)))
    else:
        crosscor = np.zeros_like(fref)
        for shift in range(len(fref)):
            crosscor[shift]=np.sum(fref * np.roll(ftest,shift))

        return crosscor