#!/usr/bin/python
"""
support for netcdf file output files containing MCA spectra
from Epics Mapping Mode with XIA xMXAP electronics
"""
import numpy as np
import time
import h5py
import sys
import os

from larch import Group, ValidateLarchPlugin

# Default tau values for xspress3

XSPRESS3_TAUS = [109.e-9, 91.e-9, 99.e-9, 98.e-9]

def estimate_icr(ocr, tau, niter=3):
    "estimate icr from ocr and tau"
    maxicr = 1.0/tau
    maxocr = 1/(tau*np.exp(1.0))
    ocr[np.where(ocr>2*maxocr)[0]] = 2*maxocr
    icr = 1.0*ocr
    for c in range(niter):
        delta = (icr - ocr*np.exp(icr*tau))/(icr*tau - 1)
        delta[np.where(delta < 0)[0]] = 0.0
        icr = icr + delta
        icr[np.where(icr>5*maxicr)[0]] = 5*maxicr
    #endfor
    return icr
#enddef


class XSP3Data(object):
    def __init__(self, npix, ndet, nchan):
        self.firstPixel   = 0
        self.numPixels    = 0
        self.realTime     = np.zeros((npix, ndet), dtype='f8')
        self.liveTime     = np.zeros((npix, ndet), dtype='f8')
        self.outputCounts = np.zeros((npix, ndet), dtype='f8')
        self.inputCounts  = np.zeros((npix, ndet), dtype='f8')
        # self.counts       = np.zeros((npix, ndet, nchan), dtype='f4')

def read_xsp3_hdf5(fname, npixels=None, verbose=False,
                   estimate_dtc=True, _larch=None):
    # Reads a HDF5 file created with the DXP xMAP driver
    # with the netCDF plugin buffers
    npixels = None
    clocktick = 12.5e-3
    t0 = time.time()
    h5file = h5py.File(fname, 'r')

    root  = h5file['entry/instrument']
    counts = root['detector/data']
    ndattr = root['detector/NDAttributes']
    # note: sometimes counts has npix-1 pixels, while the time arrays
    # really have npix...  So we take npix from the time array, and
    npix = ndattr['CHAN1SCA0'].shape[0]
    ndpix, ndet, nchan = counts.shape
    if npixels is None:
        npixels = npix
        if npixels < ndpix:
            ndpix = npixels

    out = XSP3Data(npixels, ndet, nchan)
    out.numPixels = npixels
    t1 = time.time()
    if ndpix < npix:
        out.counts = np.zeros((npix, ndet, nchan), dtype='f8')
        out.counts[:ndpix, :, :]  = counts[:]
    else:
        out.counts = counts[:]

    if estimate_dtc:
        dtc_taus = XSPRESS3_TAUS
        if _larch is not None and _larch.symtable.has_symbol('_sys.gsecars.xspress3_taus'):
            dtc_taus = _larch.symtable._sys.gsecars.xspress3_taus

    for i in range(ndet):
        rtime = clocktick * ndattr['CHAN%iSCA0' % (i+1)].value
        rtime[np.where(rtime<0.1)] = 0.1
        out.realTime[:, i] = rtime
        out.liveTime[:, i] = rtime
        ocounts = out.counts[:, i, 1:-1].sum(axis=1)
        ocounts[np.where(ocounts<0.1)] = 0.1
        out.outputCounts[:, i] = ocounts
        if estimate_dtc:
            ocr = ocounts/(rtime*1.e-6)
            icr = estimate_icr(ocr, dtc_taus[i], niter=3)
            out.inputCounts[:, i]  = icr * (rtime*1.e-6)
        else:
            out.inputCounts[:, i]  = ocounts

    h5file.close()
    t2 = time.time()
    if verbose:
        print('   time to read file    = %5.1f ms' % ((t1-t0)*1000))
        print('   time to extract data = %5.1f ms' % ((t2-t1)*1000))
        print('   read %i pixels ' %  npixels)
        print('   data shape:    ' ,  out.counts.shape)
    return out

def test_read(fname):
    print( fname,  os.stat(fname))
    fd = read_xsp3_hdf5(fname, verbose=True)
    print(fd.counts.shape)

def initializeLarchPlugin(_larch=None):
    """initialize xspress3 data"""
    g = _larch.symtable.create_group(xspress3_taus=XSPRESS3_TAUS)
    _larch.symtable.set_symbol("_sys.gsecars", g)


def registerLarchPlugin():
    return ('_xrf', {'read_xsp3_hdf5': read_xsp3_hdf5})
