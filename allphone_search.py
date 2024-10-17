# <------------------------------------------------------------------------------------------------------------------->
# <------------------------------------------------------------------------------------------------------------------->
# <------------------------------------------- (allphone_search.h) --------------------------------------------------->
# <------------------------------------------------------------------------------------------------------------------->
# <------------------------------------------------------------------------------------------------------------------->
import hmm
import ps_config
import err
import ckd_alloc
import acmod
import mdef
import bin_mdef
import fsg
import logmath
import profiles
import ngram
import strfuncs
'''
/* -*- c-basic-offset:4; indent-tabs-mode: nil -*- */
/* ====================================================================
 * Copyright (c) 2014 Carnegie Mellon University.  All rights
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
 * allphone_search.h -- Search structures for phoneme decoding.
 */
'''

#include <pocketsphinx.h>

#include "util/glist.h"
#include "util/bitvec.h"
#include "util/blkarray_list.h"
#include "lm/ngram_model.h"
#include "pocketsphinx_internal.h"
#include "hmm.h"


'''
 * Models a single unique <senone-sequence, tmat> pair.
 * Can represent several different triphones, but all with the same parent basephone.
 * (NOTE: Word-position attribute of triphone is ignored.)
typedef struct phmm_s {   } phmm_t;
'''
class phmm_s:
    hmm = hmm.hmm_t()          # hmm_t hmm;          /**< Base HMM structure */
phmm_t = phmm_s


'''
 * List of links from a PHMM node to its successors; one link per successor.
'''
# typedef struct plink_s {      } plink_t;
class plink_s:
    phmm = phmm_t()       # phmm_t *phmm;               /**< Successor PHMM node */
    # # next = plink_s()        # struct plink_s *next;       # /**< Next link for parent PHMM node */
plink_t = plink_s


'''
 * History (paths) information at any point in allphone Viterbi search.
'''
# typedef struct history_s {   } history_t;
class history_s:
    phmm = phmm_t()        # /**< PHMM ending this path */
    score = 0              # /**< Path score for this path */
    tscore = 0             # /**< Transition score for this path */
    ef = strfuncs.frame_idx_t()     # /**< End frame */
    hist = 0               # /**< Previous history entry */
history_t = history_s

'''
 * Phone level segmentation information
'''
class phseg_s:
    ci = strfuncs.s3cipid_t()          #  /* CI-phone id */
    ef = strfuncs.frame_idx_t()        # /* Start and end frame for this phone occurrence */
    sf = strfuncs.frame_idx_t()
    score = 0              # /* Acoustic score for this segment of alignment */
    tscore = 0             # /* Transition ("LM") score for this segment */
phseg_t = phseg_s

'''
 * Segment iterator over list of phseg
'''
class phseg_iter_s:
    base = ps_config.ps_seg_t()
    seg = ps_config.glist_t() 

phseg_iter_t = phseg_iter_s

'''
 * Implementation of allphone search structure.
'''

class allphone_search_s:
    base = ps_config.ps_search_t()
    
    hmmctx = hmm.hmm_context_t()   #     /**< HMM context. */
    lm = ngram.ngram_model_t()       #  /**< Ngram model set */
    ci_only = 0                # /**< Use context-independent phones for decoding */
    ci_phmm = phmm_t()         #  /**< PHMM lists (for each CI phone) */
    ci2lmwid  = 0              # int32 *ci2lmwid;          /**< Mapping of CI phones to LM word IDs */
    
    beam = 0 
    pbeam = 0                  # /**< Effective beams after applying beam_factor */
    lw = 0
    inspen = 0                 # /**< Language weights */
    
    frame = strfuncs.frame_idx_t()         #  /**< Current frame. */
    ascale = 0;                # /**< Acoustic score scale for posterior probabilities. */
    
    n_tot_frame = 0            # /**< Total number of frames processed */
    n_hmm_eval = 0             # /**< Total HMMs evaluated this utt */
    n_sen_eval = 0             # /**< Total senones evaluated this utt */
    
    # Backtrace information */
    # Hypothesis DAG */
    segments = ps_config.glist_t()
    
    perf = profiles.ptmr_t()  #  ; /**< Performance counter */

allphone_search_t = allphone_search_s

# <------------------------------------------------------------------------------------------------------------------->
# <------------------------------------------------------------------------------------------------------------------->
# <------------------------------------------- (allphone_search.c) --------------------------------------------------->
# <------------------------------------------------------------------------------------------------------------------->
# <------------------------------------------------------------------------------------------------------------------->
'''
/* -*- c-basic-offset: 4 -*- */
/* ====================================================================
 * Copyright (c) 2014 Carnegie Mellon University.  All rights
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
* allphone_search.c -- Search for phonetic decoding.
*/
'''
NULL = 0
#include <stdio.h>
#include <string.h>
#include <assert.h>

#include <pocketsphinx.h>

#include "util/ckd_alloc.h"
#include "util/strfuncs.h"
#include "util/pio.h"

#include "pocketsphinx_internal.h"
#include "allphone_search.h"

def allphone_search_lattice(search):
    return NULL

def allphone_search_prob(search):
    return 0



def allphone_search_seg_free(seg):
    ckd_alloc.ckd_free(seg)


def allphone_search_fill_iter(seg, phseg):
    seg.sf = phseg.sf
    seg.ef = phseg.ef
    seg.ascr = phseg.score
    seg.lscr = phseg.tscore
    seg.text = bin_mdef.bin_mdef_ciphone_str(acmod.ps_search_acmod(seg.search).mdef, phseg.ci)


def allphone_search_seg_next(seg):
    itor = seg
    itor.seg = itor.seg.next
    
    if (itor.seg == NULL) :
        allphone_search_seg_free(seg)
        return NULL
    
    phseg = ps_config.gnode_ptr(itor.seg)
    allphone_search_fill_iter(seg, phseg)
    
    return seg


# fsg_segfuncs = [   seg_next ,   seg_free]



def allphone_search_seg_iter(search):
    allphs = search
    phseg_iter_t *iter
    
    if (allphs.segments == NULL):
        return NULL
    
    iter = ckd_alloc.ckd_calloc(1, len(phseg_iter_t))
    
    iter.base.vt = fsg.fsg_segfuncs
    iter.base.search = search
    iter.seg = allphs.segments
    allphone_search_fill_iter(iter, ps_config.gnode_ptr(iter.seg))
    return iter


def phmm_lookup(allphs, pid):
    mdef = (allphs).acmod.mdef
    ci_phmm = allphs.ci_phmm
    p = ci_phmm[bin_mdef.bin_mdef_pid2ci(mdef, pid)]
    while(p):
        if (mdef.mdef_pid2tmatid(mdef, p.pid) == mdef.mdef_pid2tmatid(mdef, pid)):
            if (mdef.mdef_pid2ssid(mdef, p.pid) == mdef.mdef_pid2ssid(mdef, pid)):
                return p
        p = p.next
    
    return NULL



def phmm_free(allphs):
    if (~allphs.ci_phmm):
        return
    ckd_alloc.ckd_free(allphs.ci_phmm[0].lc)
    mdef = (allphs).acmod.mdef
    for ci in range(0 , mdef.mdef_n_ciphone(mdef)):
        p = allphs.ci_phmm[ci]
        while(p):
            plink_t *l, *lnext
            next = p.next
            l = p.succlist
            while(l):
                lnext = l.next
                ckd_alloc.ckd_free(l)
                l = lnext
            hmm.hmm_deinit((p.hmm))
            ckd_alloc.ckd_free(p)
            p = next
    ckd_alloc.ckd_free(allphs.ci_phmm)


def phmm_eval_all(allphs, senscr):
    mdef = (allphs).acmod.mdef
    ci_phmm = allphs.ci_phmm
    best = 1000
    hmm.hmm_context_set_senscore(allphs.hmmctx, senscr)
    for ci in range(0 , mdef.n_ciphone(mdef)):
        p = ci_phmm[ci]
        while(p):
            if (hmm.hmm_frame((p.hmm)) == allphs.frame):
                allphs.n_hmm_eval += 1
                score = hmm.hmm_vit_eval(p)
                if (score > best):
                    best = score
            p = p.next
    return best



def allphone_search_reinit(search, dict, d2p):
    allphs = search 
    if (~allphs.lm):
        err.E_WARN ("-lm argument missing; doing unconstrained phone-loop decoding\n")
        allphs.inspen = (logmath.logmath_log (search.acmod.lmath, ps_config.ps_config_float(search.config, "pip")) * allphs.lw)
    return 0


def allphone_search_free(search):
    allphs = search
    n_speech = ps_config.ps_config_int(ps_config.ps_search_config(allphs), "frate")
    ps_config.ps_search_base_free(search)
    
    hmm.hmm_context_free(allphs.hmmctx)
    hmm.phmm_free(allphs)
    if (allphs.lm):
        ngram.ngram_model_free(allphs.lm)
    if (allphs.ci2lmwid):
        ckd_alloc.ckd_free(allphs.ci2lmwid)
    if (allphs.history):
        hmm.blkarray_list_free(allphs.history)
    ckd_alloc.ckd_free(allphs)


def allphone_search_start(search):
    
    allphs = search
    mdef = search.acmod.mdef
    # Reset all HMMs. */
    for ci in range(0 , bin_mdef.bin_mdef_n_ciphone(mdef)):
        p = allphs.ci_phmm[ci]
        while(p):
            hmm.hmm_clear((p.hmm))
            p = p.next
    
    allphs.n_hmm_eval = 0
    allphs.n_sen_eval = 0
    # Free history nodes, if any */
    
    allphs.frame = 0
    ci = bin_mdef.bin_mdef_silphone(mdef)
    hmm.hmm_enter((p.hmm), 0, 0, allphs.frame)
    
    profiles.ptmr_reset(allphs.perf)
    profiles.ptmr_start(allphs.perf)
    
    return 0


def allphone_search_sen_active(allphs):
    acmod = ps_config.ps_search_acmod(allphs)
    mdef = acmod.mdef
    
    acmod.acmod_clear_active(acmod)
    for ci in range(0 , bin_mdef.bin_mdef_n_ciphone(mdef)):
        p = allphs.ci_phmm[ci]
        while(p):
            if (hmm.hmm_frame((p.hmm)) == allphs.frame):
                acmod.acmod_activate_hmm(acmod, (p.hmm))
            p = p.next


def allphone_search_step(allphs, search, frame_idx):
    acmod = search.acmod
    
    if (~acmod.compallsen):
        allphone_search_sen_active(allphs)
    senscr = acmod.acmod_score(acmod, frame_idx)
    allphs.n_sen_eval += acmod.n_senone_active
    bestscr = phmm_eval_all(allphs, senscr)
    frame_history_start = hmm.blkarray_list_n_valid(allphs.history)
    hmm.phmm_exit(allphs, bestscr)
    hmm.phmm_trans(allphs, bestscr, frame_history_start)
    
    allphs.frame += 1
    
    return 0


def ascore(allphs, h):
    score = h.score
    if (h.hist > 0):
        pred = hmm.blkarray_list_get(allphs.history, h.hist)
        score -= pred.score
    
    return score - h.tscore


def allphone_clear_segments(allphs):	
    gn = allphs.segments
    while(gn):
        ckd_alloc.ckd_free(ps_config.gnode_ptr(gn))
        gn = gn.next
    
    ps_config.glist_free(allphs.segments)
    allphs.segments = NULL

def allphone_search_finish(search):
    allphs = search
    
    allphs.n_tot_frame += allphs.frame
    n_hist = hmm.blkarray_list_n_valid(allphs.history)
    # Now backtrace. */
    profiles.ptmr_stop(allphs.perf)
    # This is the number of frames processed. */
    cf = ps_config.ps_search_acmod(allphs).output_frame
    if (cf > 0):
        n_speech = ps_config.ps_config_int(ps_config.ps_search_config(allphs), "frate")
    return 0


def allphone_search_hyp(search, out_score):
    
    allphs = search
    mdef = search.acmod.mdef
    
    # Create hypothesis */
    if (search.hyp_str):
        ckd_alloc.ckd_free(search.hyp_str)
    search.hyp_str = NULL
    if (allphs.segments == NULL):
        return NULL
    

    len = ps_config.glist_count(allphs.segments) * 10     #/* maximum length of one phone with spacebar */

    search.hyp_str = ckd_alloc.ckd_calloc(len, len(search.hyp_str))
    hyp_idx = 0
    gn = allphs.segments
    while(gn):
        p = ps_config.gnode_ptr(gn)
        phone_str = bin_mdef.bin_mdef_ciphone_str(mdef, p.ci)
        phone_idx = 0
        while (phone_str[phone_idx] != '\0'):
            search.hyp_str[hyp_idx] = phone_str[phone_idx]
        search.hyp_str[hyp_idx] = ' '
        gn.next
    
    search.hyp_str[hyp_idx] = '\0'
    return search.hyp_str

