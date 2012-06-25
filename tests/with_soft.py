from lmfit import Parameters, minimize, report_errors
from lmfit.utilfuncs import gauss
from numpy import linspace, zeros, sin, exp, random, sqrt, pi, sign
from scipy.optimize import leastsq

try:
    import matplotlib
    matplotlib.use('WXAgg')
    import pylab
    HASPYLAB = True
except ImportError:
    HASPYLAB = False

p_true = Parameters()
p_true.add('amp',  value=14.0)
p_true.add('cen',  value=5.0)
p_true.add('wid',  value=1.25)

def residual(pars, x, data=None):
    amp = pars['amp'].value
    cen = pars['cen'].value
    wid = pars['wid'].value

    model = gauss(x, amp, cen, sqrt(abs(wid)))
    if data is None:
        return model
    return (model - data)

def at_step(pars, nfev, resid, *args, **kws):
    if nfev % 100 == 0:
        print 'at step ' , nfev # args, kws
        for p in pars.values():
            print p.name, p.value

x  = linspace(0, 10, 201)
n = len(x)
noise = random.normal(scale=0.18, size=n)

data  = residual(p_true, x) + noise

fit_params = Parameters()
fit_params.add('amp', value=14.3, min=1.0, max=105.0, bounds_scale=1.0)
fit_params.add('cen', value=5.9, min=.20, max=6.5, bounds_scale=10.0)
fit_params.add('wid', value=.5)

out = minimize(residual, fit_params,
               # engine='lbfgsb',
               args=(x,), kws={'data':data})
# iter_cb=at_step)

fit = residual(fit_params, x)

print 'N fev = ', out.nfev, ' N FIT ', len(fit)
print out.chisqr, out.redchi

report_errors(fit_params, modelpars=p_true)


if HASPYLAB:
    pylab.plot(x, data, 'ro')
    pylab.plot(x, fit, 'b')
    pylab.show()





