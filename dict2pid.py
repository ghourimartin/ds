import ckd_alloc
import ps_config
import mmio
import logmath
import acmod
import dict
import bin_mdef
import err
import mdef

NULL = 0
# <------------------------------------------------------------------------------------------------------------------->
# <------------------------------------------------------------------------------------------------------------------->
# <------------------------------------------------ dict2pid.h ------------------------------------------------------->
# <------------------------------------------------------------------------------------------------------------------->
# <------------------------------------------------------------------------------------------------------------------->

'''
/* -*- c-basic-offset: 4; indent-tabs-mode: nil -*- */
/* ====================================================================
 * Copyright (c) 1999-2014 Carnegie Mellon University.  All rights
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
#ifndef _S3_DICT2PID_H_
#define _S3_DICT2PID_H_

#include <stdio.h>

#include <pocketsphinx.h>

#include "s3types.h"
#include "bin_mdef.h"
#include "dict.h"
'''
/** \file dict2pid.h
 * \brief Building triphones for a dictionary. 
 *
 * This is one of the more complicated parts of a cross-word
 * triphone model decoder.  The first and last phones of each word
 * get their left and right contexts, respectively, from other
 * words.  For single-phone words, both its contexts are from other
 * words, simultaneously.  As these words are not known beforehand,
 * life gets complicated.
 */

#ifdef __cplusplus
extern "C" {
#endif
#if 0
}
#endif

/**
 * \struct xwdssid_t
 * \brief cross word triphone model structure 
 */

typedef struct xwdssid_s {  } xwdssid_t;  
'''
class xwdssid_s:
    ssid = dict.s3ssid_t()   # s3ssid_t  *ssid;	# /**< Senone Sequence ID list for all context ciphones */
    cimap = dict.s3cipid_t() # s3cipid_t *cimap;	# /**< Index into ssid[] above for each ci phone */
    n_ssid = 0          # int32 n_ssid;	# /**< #Unique ssid in above, compressed ssid list */
xwdssid_t = xwdssid_s

'''
\struct dict2pid_t
\brief Building composite triphone (as well as word internal triphones) with the dictionary. 
'''

class dict2pid_s:
    refcount = 0               # int refcount;
    mdef = bin_mdef.bin_mdef_t()        # bin_mdef_t *mdef;           #/**< Model definition, used to generate
                                    #internal ssids on the fly. */
    dict = dict.dict_t()            # dict_t *dict;               #/**< Dictionary this table refers to. */
    
    #/* Notice the order of the arguments */
    #/* FIXME: This is crying out for compression - in Mandarin we have
    # * 180 context independent phones, which makes this an 11MB
    # * array. */
    ldiph_lc = xwdssid_s.s3ssid_t()       # s3ssid_t ***ldiph_lc;	#/**< For multi-phone words, [base][rc][lc] -> ssid; filled out for
				   #word-initial base x rc combinations in current vocabulary */
    rssid = xwdssid_t() # xwdssid_t **rssid;          #/**< Right context state sequence id table 
                                    #First dimension: base phone,
                                    #Second dimension: left context. 
                                #*/
    lrdiph_rc = xwdssid_s.s3ssid_t()      # s3ssid_t ***lrdiph_rc;      #/**< For single-phone words, [base][lc][rc] -> ssid; filled out for
                                #   single-phone base x lc combinations in current vocabulary */
    lrssid = xwdssid_t()        # xwdssid_t **lrssid;         # /**< Left-Right context state sequence id table 
                                #    First dimension: base phone,
                                #    Second dimension: left context. 
                                # */
dict2pid_t = dict2pid_s

# Access macros; not designed for arbitrary use */
#define dict2pid_rssid(d,ci,lc)  (&(d)->rssid[ci][lc])
def dict2pid_rssid(d,ci,lc):
    return ((d).rssid[ci][lc])

#define dict2pid_ldiph_lc(d,b,r,l) ((d)->ldiph_lc[b][r][l])
def dict2pid_ldiph_lc(d,b,r,l):
    return ((d).ldiph_lc[b][r][l])


#define dict2pid_lrdiph_rc(d,b,l,r) ((d)->lrdiph_rc[b][l][r])
def dict2pid_lrdiph_rc(d,b,l,r):
    return ((d).lrdiph_rc[b][l][r])


# <------------------------------------------------------------------------------------------------------------------->
# <------------------------------------------------------------------------------------------------------------------->
# <------------------------------------------------ dict2pid.c ------------------------------------------------------->
# <------------------------------------------------------------------------------------------------------------------->
# <------------------------------------------------------------------------------------------------------------------->
'''
/* -*- c-basic-offset:4; indent-tabs-mode: nil -*- */
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
#include <string.h>

#include "util/ckd_alloc.h"
#include "util/bitvec.h"
#include "s3types.h"
#include "dict2pid.h"
#include "hmm.h"


'''
 * @file dict2pid.c - dictionary word to senone sequence mappings
'''

def compress_table(uncomp_tab, com_tab, ci_map, n_ci):
    found = 0 # int32 found;
    r = 0     # int32 r;
    tmp_r = 0 # int32 tmp_r;
    
    # for (r = 0; r < n_ci; r++) {
    for r in range(0 , n_ci):
        com_tab[r] = dict.BAD_S3SSID
        ci_map[r] = dict.BAD_S3CIPID
    
    # Compress this map */
    for r in range(0 , n_ci):   # for (r = 0; r < n_ci; r++) {
        found = 0
        while(tmp_r < r and com_tab[tmp_r] != dict.BAD_S3SSID):
        # for (tmp_r = 0; tmp_r < r and com_tab[tmp_r] != BAD_S3SSID; tmp_r++)   /* If it appears before, just filled in cimap; */
            if (uncomp_tab[r] == com_tab[tmp_r]):
                found = 1
                ci_map[r] = tmp_r
                break
            
            tmp_r += 1
        
        if (found == 0):
            com_tab[tmp_r] = uncomp_tab[r]
            ci_map[r] = tmp_r




# static void compress_right_context_tree(dict2pid_t * d2p, s3ssid_t ***rdiph_rc)
def compress_right_context_tree(s3ssid_t,s3cipid_t,d2p, rdiph_rc):
    rmap = s3ssid_t() #s3ssid_t *rmap;
    tmpssid = s3ssid_t() # s3ssid_t *tmpssid;
    tmpcimap = s3cipid_t() # s3cipid_t *tmpcimap;
    mdef = d2p.mdef # bin_mdef_t *mdef = d2p->mdef;
    
    n_ci = mdef.n_ciphone
    
    tmpssid = ckd_alloc.ckd_calloc(n_ci, len(s3ssid_t))
    tmpcimap = ckd_alloc.ckd_calloc(n_ci, len(s3cipid_t))
    
    d2p.rssid = ckd_alloc.ckd_calloc(mdef.n_ciphone, len(xwdssid_t))
    alloc = mdef.n_ciphone * len(xwdssid_t)
    
    for b in range(0 , n_ci):
        d2p.ssid[b] = ckd_alloc.ckd_calloc(mdef.n_ciphone, len(xwdssid_t))
        alloc += mdef.n_ciphone * len(xwdssid_t)
        
        for l in range(0 ,  n_ci):
            rmap = rdiph_rc[b][l]
            compress_table(rmap, tmpssid, tmpcimap, mdef.n_ciphone)
            
            r = 0
            while(r < mdef.n_ciphone and tmpssid[r] != dict.BAD_S3SSID):
                if (tmpssid[0] != dict.BAD_S3SSID):
                    d2p.rssid[b][l].ssid = ckd_alloc.ckd_calloc(r, len(s3ssid_t))
                    d2p.rssid[b][l].cimap = ckd_alloc.ckd_calloc(mdef.n_ciphone, len(s3cipid_t))
                    d2p.rssid[b][l].n_ssid = r
                
                else:
                    d2p.rssid[b][l].ssid = NULL
                    d2p.rssid[b][l].cimap = NULL
                    d2p.rssid[b][l].n_ssid = 0
                r += 1
    
    
    
    err.E_INFO(f"Allocated {alloc} bytes ({alloc / 1024} KiB) for word-final triphones\n")
    ckd_alloc.ckd_free(tmpssid)
    ckd_alloc.ckd_free(tmpcimap)


# static void compress_left_right_context_tree(dict2pid_t * d2p)
def compress_left_right_context_tree(s3ssid_t , d2p):
    n_ci = 0
    b = 0
    l = 0
    r = 0
    
    mdef = d2p.mdef
    
    
    n_ci = mdef.n_ciphone
    
    tmpssid = ckd_alloc.ckd_calloc(n_ci, len(s3ssid_t))
    tmpcimap = ckd_alloc.ckd_calloc(n_ci, len(d2p))
    
    assert(d2p.lrdiph_rc)
    
    d2p.lrssid = ckd_alloc.ckd_calloc(mdef.n_ciphone, len(xwdssid_t))
    alloc = mdef.n_ciphone * len(xwdssid_t)
    
    for b in range(0 , n_ci):  #     for (b = 0; b < n_ci; b++) {
        
        d2p.lrssid[b] = ckd_alloc.ckd_calloc(mdef.n_ciphone, len(xwdssid_t))
        alloc += mdef.n_ciphone * len(xwdssid_t)
        
        for i in range(0 , n_ci):    # for (l = 0; l < n_ci; l++) {
            
            rmap = d2p.lrdiph_rc[b][l]
            
            compress_table(rmap, tmpssid, tmpcimap, mdef.n_ciphone)
            r = 0
            while (r < mdef.n_ciphone and tmpssid[r] != dict.BAD_S3SSID):   # for (r = 0; r < mdef->n_ciphone && tmpssid[r] != BAD_S3SSID; r++);
                r += 1
            
            if (tmpssid[0] != dict.BAD_S3SSID):
                d2p.lrssid[b][l].ssid = ckd_alloc.ckd_calloc(r, len(s3ssid_t))
                d2p.lrssid[b][l].cimap = ckd_alloc.ckd_calloc(mdef.n_ciphone, len(s3ssid_t))
                d2p.lrssid[b][l].n_ssid = r
            
            else:
                d2p.lrssid[b][l].ssid = NULL
                d2p.lrssid[b][l].cimap = NULL
                d2p.lrssid[b][l].n_ssid = 0
    
    # Try to compress lrdiph_rc into lrdiph_rc_compressed */
    ckd_alloc.ckd_free(tmpssid)
    ckd_alloc.ckd_free(tmpcimap)


'''/**
 * Get number of rc 
 */
int32 get_rc_nssid(dict2pid_t *d2p,  /**< In: a dict2pid */
		   s3wid_t w         /**< In: a wid */
    );
    

   ARCHAN, A duplicate of get_rc_npid in ctxt_table.h.  I doubt whether it is correct
   because the compressed map has not been checked. 
'''
def get_rc_nssid(d2p,w):
    dict = d2p.dict
    
    pronlen = dict.word[w].pronlen
    b = dict.word[w].ciphone[pronlen - 1]
    
    if (pronlen == 1):
        ''' Is this true ?
        No known left context.  But all cimaps (for any l) are identical; pick one 
        */
        /*E_INFO("Single phone word\n"); '''
        return (d2p.lrssid[b][0].n_ssid)
    
    else:
        #    E_INFO("Multiple phone word\n"); */
        lc = dict.word[w].ciphone[pronlen - 2]
        return (d2p.rssid[b][lc].n_ssid)




'''/**
 * Get RC map 
 */
s3cipid_t* dict2pid_get_rcmap(dict2pid_t *d2p,  /**< In: a dict2pid */
			      s3wid_t w        /**< In: a wid */
    );
    
'''

def dict2pid_get_rcmap(d2p, w):
    dict = d2p.dict
    
    pronlen = dict.word[w].pronlen
    b = dict.word[w].ciphone[pronlen - 1]
    
    if (pronlen == 1):
        ''' Is this true ?
        No known left context.  But all cimaps (for any l) are identical; pick one 
        */
        /*E_INFO("Single phone word\n"); '''
        return (d2p.lrssid[b][0].cimap)
    
    else:
        #    E_INFO("Multiple phone word\n") */
        lc = dict.word[w].ciphone[pronlen - 2]
        return (d2p.rssid[b][lc].cimap)



def free_compress_map(tree, n_ci):
    for b in range(0 , n_ci):
        for l in range(0 , n_ci):
            ckd_alloc.ckd_free(tree[b][l].ssid)
            ckd_alloc.cckd_free(tree[b][l].cimap)
        ckd_alloc.cckd_free(tree[b])
    ckd_alloc.ckd_free(tree)


# static void populate_lrdiph(dict2pid_t *d2p, s3ssid_t ***rdiph_rc, s3cipid_t b)
def populate_lrdiph(d2p, rdiph_rc, b):
    mdef = d2p.mdef
    
    
    #for (l = 0; l < bin_mdef_n_ciphone(mdef); l++):
    for l in range(0 , bin_mdef.bin_mdef_n_ciphone(mdef)):
        for r in range(0 , bin_mdef.bin_mdef_n_ciphone(mdef)):  # for (r = 0; r < bin_mdef_n_ciphone(mdef); r++) {
            p = bin_mdef.bin_mdef_phone_id_nearest(mdef, b, l, r, mdef.WORD_POSN_SINGLE)
            d2p.lrdiph_rc[b][l][r] = mdef.bin_mdef_pid2ssid(mdef, p)
            if (r == bin_mdef.bin_mdef_silphone(mdef)):
                d2p.ldiph_lc[b][r][l] = bin_mdef.bin_mdef_pid2ssid(mdef, p)
            if (rdiph_rc and l == bin_mdef.bin_mdef_silphone(mdef)):
                rdiph_rc[b][l][r] = bin_mdef.bin_mdef_pid2ssid(mdef, p)
            assert(mdef.IS_S3SSID(bin_mdef.bin_mdef_pid2ssid(mdef, p)))
            err.E_DEBUG("%s(%s,%s) => %d / %d\n", bin_mdef.bin_mdef_ciphone_str(mdef, b), bin_mdef.bin_mdef_ciphone_str(mdef, l), bin_mdef.bin_mdef_ciphone_str(mdef, r), p, mdef.bin_mdef_pid2ssid(mdef, p))


'''/**
 * Add a word to the dict2pid structure (after adding it to dict).
 */
int dict2pid_add_word(dict2pid_t *d2p, int32 wid); '''

def dict2pid_add_word(d2p, wid):
    mdef = d2p.mdef
    d = d2p.dict
    
    if (dict.dict_pronlen(d, wid) > 1): 
        # Make sure we have left and right context diphones for this word. 
        if (d2p.ldiph_lc[dict.dict_first_phone(d, wid)][dict.dict_second_phone(d, wid)][0] == dict.BAD_S3SSID):
            err.E_DEBUG("Filling in left-context diphones for %s(?,%s)\n", mdef.bin_mdef_ciphone_str(mdef, dict.dict_first_phone(d, wid)), mdef.bin_mdef_ciphone_str(mdef, dict.dict_second_phone(d, wid)))
            for l in range(0 , mdef.bin_mdef_n_ciphone(mdef)):   #             for (l = 0; l < bin_mdef_n_ciphone(mdef); l++):
                p = mdef.bin_mdef_phone_id_nearest(mdef, dict.dict_first_phone(d, wid), l, dict.dict_second_phone(d, wid), dict.WORD_POSN_BEGIN)
                d2p.ldiph_lc[dict.dict_first_phone(d, wid)][dict.dict_second_phone(d, wid)][l] = mdef.bin_mdef_pid2ssid(mdef, p)
        
        
        if (d2p.rssid[dict.dict_last_phone(d, wid)][dict.dict_second_last_phone(d, wid)].n_ssid == 0):
            
            err.E_DEBUG("Filling in right-context diphones for %s(%s,?)\n", bin_mdef.bin_mdef_ciphone_str(mdef, dict.dict_last_phone(d, wid)), bin_mdef.bin_mdef_ciphone_str(mdef, dict.dict_second_last_phone(d, wid)))
            rmap = ckd_alloc.ckd_calloc(bin_mdef.bin_mdef_n_ciphone(mdef), len(rmap))
            for r in range(0 , bin_mdef.bin_mdef_n_ciphone(mdef)):      #  for (r = 0; r < bin_mdef_n_ciphone(mdef); r++) {
                p = bin_mdef.bin_mdef_phone_id_nearest(mdef, dict.dict_last_phone(d, wid), dict.dict_second_last_phone(d, wid), r, dict.WORD_POSN_END)
                rmap[r] = bin_mdef.bin_mdef_pid2ssid(mdef, p)
            
            tmpssid = ckd_alloc.ckd_calloc(bin_mdef.bin_mdef_n_ciphone(mdef), len(tmpssid))
            tmpcimap = ckd_alloc.ckd_calloc(bin_mdef.bin_mdef_n_ciphone(mdef), len(tmpcimap))
            compress_table(rmap, tmpssid, tmpcimap, bin_mdef.bin_mdef_n_ciphone(mdef))
            d2p.rssid[dict.dict_last_phone(d, wid)][dict.dict_second_last_phone(d, wid)].ssid = tmpssid
            d2p.rssid[dict.dict_last_phone(d, wid)][dict.dict_second_last_phone(d, wid)].cimap = tmpcimap
            d2p.rssid[dict.dict_last_phone(d, wid)][dict.dict_second_last_phone(d, wid)].n_ssid = r
            ckd_alloc.ckd_free(rmap)
    
    else:
        # Make sure we have a left-right context triphone entry for this word. */
        err.E_INFO("Filling in context triphones for %s(?,?)\n", bin_mdef.bin_mdef_ciphone_str(mdef, dict.dict_first_phone(d, wid)))
        if (d2p.lrdiph_rc[dict.dict_first_phone(d, wid)][0][0] == dict.BAD_S3SSID):
            populate_lrdiph(d2p, NULL, dict.dict_first_phone(d, wid))
    
    return 0


'''/**
 * Return the senone sequence ID for the given word position.
 */
s3ssid_t dict2pid_internal(dict2pid_t *d2p, int32 wid, int pos); '''

def dict2pid_internal(d2p, wid, pos):
    dict = d2p.dict
    mdef = d2p.mdef
    
    if (pos == 0 or pos == dict.dict_pronlen(dict, wid)):
        return dict.BAD_S3SSID
    
    b = dict.dict_pron(dict, wid, pos)
    l = dict.dict_pron(dict, wid, pos - 1)
    r = dict.dict_pron(dict, wid, pos + 1)
    p = bin_mdef.bin_mdef_phone_id_nearest(mdef, b, l, r, dict.WORD_POSN_INTERNAL)
    return bin_mdef.bin_mdef_pid2ssid(mdef, p)


'''/**
 * Build the dict2pid structure for the given model/dictionary
 */
dict2pid_t *dict2pid_build(bin_mdef_t *mdef,   /**< A  model definition*/
                           dict_t *dict        /**< An initialized dictionary */
    );
    '''
def dict2pid_build(s3ssid_t, mdef, dict):
    err.E_INFO("Building PID tables for dictionary\n")
    assert(mdef)
    assert(dict)
    
    dict2pid = ckd_alloc.ckd_calloc(1, len(dict2pid_t))
    dict2pid.refcount = 1
    dict2pid.mdef = bin_mdef.bin_mdef_retain(mdef)
    dict2pid.dict = dict.dict_retain(dict)
    dict2pid.ldiph_lc = ckd_alloc.ckd_calloc_3d(mdef.n_ciphone, mdef.n_ciphone, mdef.n_ciphone, len(s3ssid_t))
    # Only used internally to generate rssid */
    rdiph_rc = ckd_alloc.ckd_calloc_3d(mdef.n_ciphone, mdef.n_ciphone, mdef.n_ciphone, len(s3ssid_t))
    
    dict2pid.lrdiph_rc = ckd_alloc.ckd_calloc_3d(mdef.n_ciphone, mdef.n_ciphone, mdef.n_ciphone, len(s3ssid_t))
    # Actually could use memset for this, if BAD_S3SSID is guaranteed
    # to be 65535... */
    for b in range(0 , mdef.n_ciphone):                    #  for (b = 0; b < mdef->n_ciphone; ++b) {
        for r in range(0 , mdef.n_ciphone):                # for (r = 0; r < mdef->n_ciphone; ++r) {
            for l in range(0 , mdef.n_ciphone):            # for (l = 0; l < mdef->n_ciphone; ++l) {
                dict2pid.ldiph_lc[b][r][l] = dict.BAD_S3SSID
                dict2pid.lrdiph_rc[b][l][r] = dict.BAD_S3SSID
                rdiph_rc[b][l][r] = dict.BAD_S3SSID
    
    
    
    
    # Track which diphones / ciphones have been seen. */
    ldiph = ckd_alloc.bitvec_alloc(mdef.n_ciphone * mdef.n_ciphone)
    rdiph = ckd_alloc.bitvec_alloc(mdef.n_ciphone * mdef.n_ciphone)
    single = ckd_alloc.bitvec_alloc(mdef.n_ciphone)
    
    for w in range(0 , dict.dict_size(dict2pid.dict)):   # for (w = 0; w < dict_size(dict2pid->dict); w++)
        pronlen = dict.dict_pronlen(dict, w)
        
        if (pronlen >= 2):
            b = dict.dict_first_phone(dict, w)
            r = dict.dict_second_phone(dict, w)
            # Populate ldiph_lc */
            if (ckd_alloc.bitvec_is_clear(ldiph, b * mdef.n_ciphone + r)):
                # Mark this diphone as done */
                ckd_alloc.bitvec_set(ldiph, b * mdef.n_ciphone + r)
                
                # Record all possible ssids for b(?,r) */
                for l in range(0, bin_mdef.bin_mdef_n_ciphone(mdef)): # for (l = 0; l < bin_mdef_n_ciphone(mdef); l++) {
                    p = bin_mdef.bin_mdef_phone_id_nearest(mdef,b, l, r, dict.WORD_POSN_BEGIN)
                    dict2pid.ldiph_lc[b][r][l] = bin_mdef.bin_mdef_pid2ssid(mdef, p)
            
            # Populate rdiph_rc */
            l = dict.dict_second_last_phone(dict, w)
            b = dict.dict_last_phone(dict, w)
            if (ckd_alloc.bitvec_is_clear(rdiph, b * mdef.n_ciphone + l)):
                # Mark this diphone as done */
                ckd_alloc.bitvec_set(rdiph, b * mdef.n_ciphone + l)
                
                for r in range(0 , bin_mdef.bin_mdef_n_ciphone(mdef)):     # for (r = 0; r < bin_mdef_n_ciphone(mdef); r++) {
                    p = bin_mdef.bin_mdef_phone_id_nearest(mdef, b, l, r,  dict.WORD_POSN_END)
                    rdiph_rc[b][l][r] = bin_mdef.bin_mdef_pid2ssid(mdef, p)
        
        elif(pronlen == 1):
            b = dict.dict_pron(dict, w, 0)
            # Populate lrdiph_rc (and also ldiph_lc, rdiph_rc if needed) */
            if (ckd_alloc.bitvec_is_clear(single, b)):
                populate_lrdiph(dict2pid, rdiph_rc, b)
                ckd_alloc.bitvec_set(single, b)
    
    ckd_alloc.bitvec_free(ldiph)
    ckd_alloc.bitvec_free(rdiph)
    ckd_alloc.bitvec_free(single)
    
    # Try to compress rdiph_rc into rdiph_rc_compressed */
    compress_right_context_tree(dict2pid, rdiph_rc)
    compress_left_right_context_tree(dict2pid)
    
    ckd_alloc.ckd_free_3d(rdiph_rc)
    
    return dict2pid


'''/**
 * Retain a pointer to dict2pid
 */
dict2pid_t *dict2pid_retain(dict2pid_t *d2p);  
'''

def dict2pid_retain(d2p):
    d2p.refcount += 1
    return d2p


'''/**
 * Free the memory dict2pid structure
 */
int dict2pid_free(dict2pid_t *d2p /**< In: the d2p */
    );
    '''
# int dict2pid_free(dict2pid_t * d2p)
def dict2pid_free(d2p):
    if (d2p == NULL):
        return 0
    if (d2p.refcount-1 > 0):
        return d2p.refcount
    
    if (d2p.ldiph_lc):
        ckd_alloc.ckd_free_3d(d2p.ldiph_lc)
    
    if (d2p.lrdiph_rc):
        ckd_alloc.ckd_free_3d(d2p.lrdiph_rc)
    
    if (d2p.rssid):
        free_compress_map(d2p.rssid, bin_mdef.bin_mdef_n_ciphone(d2p.mdef))
    
    if (d2p.lrssid):
        free_compress_map(d2p.lrssid, bin_mdef.bin_mdef_n_ciphone(d2p.mdef))
    
    bin_mdef.bin_mdef_free(d2p.mdef)
    dict.dict_free(d2p.dict)
    ckd_alloc.ckd_free(d2p)
    return 0


'''/**
 * For debugging
 */
void dict2pid_dump(FILE *fp,        /**< In: a file pointer */
                   dict2pid_t *d2p /**< In: a dict2pid_t structure */
    );
    '''
def dict2pid_dump(fp, d2p):
    mdef = d2p.mdef
    dict = d2p.dict
    for w in range(0 , dict.dict_size(dict)):
        pronlen = dict.dict_pronlen(dict, w)



