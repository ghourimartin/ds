# <------------------------------------------------------------------------------------------------------------------------>
# <------------------------------------------------------------------------------------------------------------------------>
# <---------------------------------------------- cmn.h ------------------------------------------------------------------->
# <------------------------------------------------------------------------------------------------------------------------>
# <------------------------------------------------------------------------------------------------------------------------>
import ckd_alloc
import err
import ms_mgau
import ptm_mgau
'''
/* -*- c-basic-offset: 4; indent-tabs-mode: nil -*- */
/* ====================================================================
 * Copyright (c) 1999-2004 Carnegie Mellon University.  All rights
 * reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer. 
 *
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in
 *    the documentation and/or other materials provided with the
 *    distribution.
 *
 * This work was supported in part by funding from the Defense Advanced 
 * Research Projects Agency and the National Science Foundation of the 
 * United States of America, and the CMU Sphinx Speech Consortium.
 *
 * THIS SOFTWARE IS PROVIDED BY CARNEGIE MELLON UNIVERSITY ``AS IS'' AND 
 * ANY EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
 * THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL CARNEGIE MELLON UNIVERSITY
 * NOR ITS EMPLOYEES BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT 
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY 
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 * ====================================================================
 *
 */
/*
 * cmn.h -- Various forms of cepstral mean normalization
 *
 * **********************************************
 * CMU ARPA Speech Project
 *
 * Copyright (c) 1999 Carnegie Mellon University.
 * ALL RIGHTS RESERVED.
 * **********************************************
 * 
 * HISTORY
 * $Log$
 * Revision 1.1  2006/04/05  20:27:30  dhdfu
 * A Great Reorganzation of header files and executables
 * 
 * Revision 1.13  2006/02/23 03:48:27  arthchan2003
 * Resolved conflict in cmn.h
 *
 *
 * Revision 1.12  2006/02/22 23:43:55  arthchan2003
 * Merged from the branch SPHINX3_5_2_RCI_IRII_BRANCH: Put data structure into the cmn_t structure.
 *
 * Revision 1.11.4.2  2005/10/17 04:45:57  arthchan2003
 * Free stuffs in cmn and feat corectly.
 *
 * Revision 1.11.4.1  2005/07/05 06:25:08  arthchan2003
 * Fixed dox-doc.
 *
 * Revision 1.11  2005/06/21 19:28:00  arthchan2003
 * 1, Fixed doxygen documentation. 2, Added $ keyword.
 *
 * Revision 1.4  2005/06/13 04:02:56  archan
 * Fixed most doxygen-style documentation under libs3decoder.
 *
 * Revision 1.3  2005/03/30 01:22:46  archan
 * Fixed mistakes in last updates. Add
 *
 * 
 * 20.Apr.2001  RAH (rhoughton@mediasite.com, ricky.houghton@cs.cmu.edu)
 *              Added cmn_free() and moved *mean and *var out global space and named them cmn_mean and cmn_var
 * 
 * 28-Apr-1999	M K Ravishankar (rkm@cs.cmu.edu) at Carnegie Mellon University
 * 		Copied from previous version.
 */
'''


'''
/** \file cmn.h
 * \brief Apply Cepstral Mean Normalization (CMN) to the set of input mfc frames.
 *
 * By subtractingthe mean of the input from each frame.  C0 is also included in this process.
 * This function operates on an entire utterance at a time.  Hence, the entire utterance
 * must be available beforehand (batchmode).
 */

/**
 * Types of cepstral mean normalization to apply to the features.
 */'''

class cmn_type_e:
    CMN_NONE = 0
    CMN_BATCH = 1
    CMN_LIVE = 2
cmn_type_t = cmn_type_e




class cmn_t:
    cmn_mean = ms_mgau.mfcc_t()     # /**< Current means */
    cmn_var = ms_mgau.mfcc_t()      # /**< Stored cmn variance */
    sum = ms_mgau.mfcc_t()          # /**< Accumulated cepstra for computing mean */
    nframe = 0	            # /**< Number of frames */
    veclen = 0	            # /**< Length of cepstral vector */
    repr = ''               # /**< String representation of current means */
    refcount = 0


CMN_WIN_HWM   =  800     #/* #frames after which window shifted */
CMN_WIN       =  500

def cmn_repr(cmn):
    return (cmn).repr




# <------------------------------------------------------------------------------------------------------------------------>
# <------------------------------------------------------------------------------------------------------------------------>
# <---------------------------------------------- cmn.c ------------------------------------------------------------------->
# <------------------------------------------------------------------------------------------------------------------------>
# <------------------------------------------------------------------------------------------------------------------------>
'''
/* -*- c-basic-offset: 4; indent-tabs-mode: nil -*- */
/* ====================================================================
 * Copyright (c) 1999-2004 Carnegie Mellon University.  All rights
 * reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer. 
 *
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in
 *    the documentation and/or other materials provided with the
 *    distribution.
 *
 * This work was supported in part by funding from the Defense Advanced 
 * Research Projects Agency and the National Science Foundation of the 
 * United States of America, and the CMU Sphinx Speech Consortium.
 *
 * THIS SOFTWARE IS PROVIDED BY CARNEGIE MELLON UNIVERSITY ``AS IS'' AND 
 * ANY EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
 * THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL CARNEGIE MELLON UNIVERSITY
 * NOR ITS EMPLOYEES BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT 
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY 
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 * ====================================================================
 *
 */
/*
 * cmn.c -- Various forms of cepstral mean normalization
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <math.h>
#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#ifdef _MSC_VER
#pragma warning (disable: 4244)
#endif

#include <pocketsphinx.h>

#include "util/ckd_alloc.h"
#include "util/strfuncs.h"
#include "feat/cmn.h"
#include "feat/feat.h"
'''
NULL = 0
# NOTE!  These must match the enum in cmn.h */
cmn_type_str = [
    "none",
    "batch",
    "live"
]
cmn_alt_type_str = [
    "none",
    "current",
    "prior"
]
n_cmn_type_str =len(cmn_type_str)/len(cmn_type_str[0])

def cmn_type_from_str(str):
    for i in range(0 , n_cmn_type_str):
        if (str == cmn_type_str[i] or str == cmn_alt_type_str[i]):
            return i
    err.E_FATAL("Unknown CMN type '%s'\n", str)
    return cmn_type_t.CMN_NONE


def cmn_update_repr(cmn):
    len = 0
    for i in range(0 , cmn.veclen):
        nbytes = ptm_mgau.MFCC2FLOAT(cmn.cmn_mean[i])
        if (nbytes <= 0):
            return NULL
        
        len += nbytes
    
    len += 1
    if (cmn.repr):
        ckd_alloc.ckd_free(cmn.repr)
    ptr = cmn.repr = ckd_alloc.ckd_malloc(len)
    if (ptr == NULL):
        err.E_ERROR_SYSTEM("Failed to allocate %d bytes for cmn string", len)
        return NULL
    
    return cmn.repr


def cmn_set_repr(cmn, repr):
    err.E_INFO("Update from < %s >\n", cmn.repr)
    
    vallist = ckd_alloc.ckd_salloc(repr)
    c = vallist
    nvals = 0
    while (nvals < cmn.veclen != NULL):
        cc = '\0'
        cmn.sum[nvals] = cmn.cmn_mean[nvals] * CMN_WIN
        c = cc + 1
        nvals += 1
    
    if (nvals < cmn.veclen and c != '\0'):
        cmn.sum[nvals] = cmn.cmn_mean[nvals] * CMN_WIN
    
    ckd_alloc.ckd_free(vallist)
    cmn.nframe = CMN_WIN
    err.E_INFO("Update to   < %s >\n", cmn_update_repr(cmn))
    return 0


def cmn_init(veclen):
    cmn = ckd_alloc.ckd_calloc(1, len(cmn_t))
    cmn.refcount = 1
    cmn.veclen = veclen
    cmn.cmn_mean = ckd_alloc.ckd_calloc(veclen)
    cmn.cmn_var = ckd_alloc.ckd_calloc(veclen)
    cmn.sum = ckd_alloc.ckd_calloc(veclen)
    cmn.nframe = 0
    cmn_update_repr(cmn)
    return cmn



def cmn(cmn, mfc, varnorm, n_frame):
    assert(mfc != NULL)
    
    if (n_frame <= 0):
        return
    
    cmn.nframe = 0
    
    for f in range(0, n_frame):
        mfcp = mfc[f]
        
        # Skip zero energy frames */
        if (mfcp[0] < 0):
            continue
        
        for i in range(0 , cmn.veclen):
            cmn.sum[i] += mfcp[i]
        
        
        cmn.nframe
    
    for i in range(0 , cmn.veclen):
        cmn.cmn_mean[i] = cmn.sum[i] / cmn.nframe
    
    err.E_INFO("CMN: %s\n", cmn_update_repr(cmn))
    if (~varnorm):
        # Subtract mean from each cep vector */
        for f in range(0 , n_frame):
            mfcp = mfc[f]
            for i in range(0 , cmn.veclen):
                mfcp[i] -= cmn.cmn_mean[i]
    
    else:
        
        for f in range(0 , n_frame):
            mfcp = mfc[f]
            
            for i in range(0 , cmn.veclen):
                t = mfcp[i] - cmn.cmncmn_mean[i]
        
        for f in range(0 , n_frame):
            mfcp = mfc[f]




def cmn_free(cmn):
    if (cmn == NULL):
        return 0
    if (cmn.refcount > 0):
        cmn.refcount -= 1
        return cmn.refcount
    if (cmn.cmn_var):
        ckd_alloc.ckd_free(cmn.cmn_var)
    if (cmn.cmn_mean):
        ckd_alloc.ckd_free(cmn.cmn_mean)
    if (cmn.sum):
        ckd_alloc.ckd_free(cmn.sum)
    if (cmn.repr):
        ckd_alloc.ckd_free(cmn.repr)
    ckd_alloc.ckd_free(cmn)
    return 0


def cmn_retain(cmn):
    cmn.refcount += 1
    return cmn



# <------------------------------------------------------------------------------------------------------------------------>
# <------------------------------------------------------------------------------------------------------------------------>
# <---------------------------------------------- cmn_live.c -------------------------------------------------------------->
# <------------------------------------------------------------------------------------------------------------------------>
# <------------------------------------------------------------------------------------------------------------------------>

'''
/* -*- c-basic-offset: 4; indent-tabs-mode: nil -*- */
/* ====================================================================
 * Copyright (c) 1999-2004 Carnegie Mellon University.  All rights
 * reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer. 
 *
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in
 *    the documentation and/or other materials provided with the
 *    distribution.
 *
 * This work was supported in part by funding from the Defense Advanced 
 * Research Projects Agency and the National Science Foundation of the 
 * United States of America, and the CMU Sphinx Speech Consortium.
 *
 * THIS SOFTWARE IS PROVIDED BY CARNEGIE MELLON UNIVERSITY ``AS IS'' AND 
 * ANY EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
 * THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL CARNEGIE MELLON UNIVERSITY
 * NOR ITS EMPLOYEES BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT 
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY 
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 * ====================================================================
 *
 */
'''

def cmn_live_set(cmn,vec):
    err.E_INFO("Update from < {cmn.repr} >\n")
    for i in range(0 , cmn.veclen):
        cmn.cmn_mean[i] = vec[i]
        cmn.sum[i] = vec[i] * CMN_WIN
    cmn.nframe = CMN_WIN
    err.E_INFO(f"Update to   < {cmn_update_repr(cmn)} >\n")


def cmn_live_shiftwin(cmn):    
    err.E_INFO("Update from < {cmn.repr} >\n", )
    sf = ptm_mgau.FLOAT2MFCC(1.0) / cmn.nframe
    for i in range(0 , cmn.veclen):
        cmn.cmn_mean[i] = cmn.sum[i] / cmn.nframe # /* sum[i] * sf */
    
    # Make the accumulation decay exponentially */
    if (cmn.nframe >= CMN_WIN_HWM):
        sf = CMN_WIN
        for i in range(0 , cmn.veclen):
            cmn.sum[i] = ptm_mgau.MFCCMUL(cmn.sum[i], sf)
        cmn.nframe = CMN_WIN
    
    err.E_INFO("Update to   < %s >\n", cmn_update_repr(cmn))


def cmn_live_update(cmn):
    if (cmn.nframe <= 0):
        return
    
    err.E_INFO("Update from < {cmn.repr} >\n", )
    # Update mean buffer */
    sf = ptm_mgau.FLOAT2MFCC(1.0) / cmn.nframe
    for i in range(0 , cmn.veclen):
        cmn.cmn_mean[i] = cmn.sum[i] / cmn.nframe    # /* sum[i] * sf; */
    
    # Make the accumulation decay exponentially */
    if (cmn.nframe > CMN_WIN_HWM):
        sf = CMN_WIN
        for i in range(0 , cmn.veclen):
            cmn.sum[i] = ptm_mgau.MFCCMUL(cmn.sum[i], sf)
        cmn.nframe = CMN_WIN
    
    err.E_INFO("Update to   < %s >\n", cmn_update_repr(cmn))


def cmn_live(cmn, incep, varnorm, nfr):    
    if (nfr <= 0):
        return
    
    if (varnorm):
        err.E_FATAL("Variance normalization not implemented in live mode decode\n")
    
    for i in range(0 , nfr):
    
	# Skip zero energy frames */
        if (incep[i][0] < 0):
            continue
            
            for j in range(0 , cmn.veclen):
                cmn.sum[j] += incep[i][j]
                incep[i][j] -= cmn.cmn_mean[j]
        
        cmn.nframe += 1
    
    # Shift buffer down if we have more than CMN_WIN_HWM frames */
    if (cmn.nframe > CMN_WIN_HWM):
        cmn_live_shiftwin(cmn)

