# <------------------------------------------------------------------------------------------------------------------->
# <------------------------------------------------------------------------------------------------------------------->
# <------------------------------------------- (bin_mdef.h) ---------------------------------------------------------->
# <------------------------------------------------------------------------------------------------------------------->
# <------------------------------------------------------------------------------------------------------------------->
'''
/* -*- c-file-style: "linux" -*- */
/* ====================================================================
 * Copyright (c) 2005 Carnegie Mellon University.  All rights 
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
/**
 * @file bin_mdef.h
 * 
 * Binary format model definition files, with support for
 * heterogeneous topologies and variable-size N-phones
 *
 * @author David Huggins-Daines <dhdaines@gmail.com>
'''
import ckd_alloc
import err
import mmio
'''
 * Phone entry (on-disk, 12 bytes)
'''


class mdef_entry_s:
	ssid = 0      #  /**< Senone sequence ID */
	tmat = 0      #  /**< Transition matrix ID */

class ci:
	filler = 0
	reserved = [0]*3
		
class cd:
	wpos = 0
	ctx = [0]*3   #  /**< quintphones will require hacking */
class info:
    wpos = 0


mdef_entry_t = mdef_entry_s


BAD_SSID = 0xffff


BAD_SENID = 0xffff


class cd_tree_s:
	ctx = 0        # /**< Context (word position or CI phone) */
	n_down = 0     # /**< Number of children (0 for leafnode) */
	class c:
		pid = 0      # /**< Phone ID (leafnode) */
		down = 0     #  /**< Next level of the tree (offset from start of cd_trees) */ 


cd_tree_t = cd_tree_s


class bin_mdef_s:
	refcnt = 0
	n_ciphone = 0            # /**< Number of base (CI) phones */
	n_phone = 0	             # /**< Number of base (CI) phones + (CD) triphones */
	n_emit_state = 0         # /**< Number of emitting states per phone (0 for heterogeneous) */
	n_ci_sen = 0	         # /**< Number of CI senones; these are the first */
	n_sen = 0	             # /**< Number of senones (CI+CD) */
	n_tmat = 0	             # /**< Number of transition matrices */
	n_sseq = 0               # /**< Number of unique senone sequences */
	n_ctx = 0	             # /**< Number of phones of context */
	n_cd_tree = 0            # /**< Number of nodes in cd_tree (below) */
	sil = 0	                 # /**< CI phone ID for silence */
    
	filemap = mmio.mmio_file_t()  # /**< File map for this file (if any) */
	ciname = ''              # /**< CI phone names */
	phone = mdef_entry_t()   # /**< All phone structures */
	sseq = 0                 # /**< Unique senone sequences (2D array built at load time) */
	sseq_len = 0             # /**< Number of states in each sseq (NULL for homogeneous) */
    
	# These two are not stored on disk, but are generated at load time. */
    BIN_MDEF_FROM_TEXT = 0
	cd2cisen = 0	         # /**< Parent CI-senone id for each senone */
	sen2cimap = 0	         # /**< Parent CI-phone for each senone (CI or CD) */
    N_WORD_POSN = 0
	BIN_MDEF_FROM_TEXT = 0 
    BIN_MDEF_IN_MEMORY = 1 
    BIN_MDEF_ON_DISK = 3 
    alloc_mode = 4

bin_mdef_t = bin_mdef_s

def bin_mdef_is_fillerphone(m,p):
    return (((p) < (m).n_ciphone) if (m).phone[p].info.ci.filler else (m).phone[(m).phone[p].info.cd.ctx[0]].info.ci.filler)
def bin_mdef_is_ciphone(m,p):
    return ((p) < (m).n_ciphone)
def bin_mdef_n_ciphone(m):
    return ((m).n_ciphone)
def bin_mdef_n_phone(m):
    return ((m).n_phone)
def bin_mdef_n_sseq(m):
    return ((m).n_sseq)
def bin_mdef_n_emit_state(m):
    return ((m).n_emit_state)
def bin_mdef_n_emit_state_phone(m,p):
    return ((m).n_emit_state if (m).n_emit_state else (m).sseq_len[(m).phone[p].ssid])
def bin_mdef_n_sen(m):
    return ((m).n_sen)
def bin_mdef_n_tmat(m):
    return ((m).n_tmat)
def bin_mdef_pid2ssid(m,p):
    return ((m).phone[p].ssid)
def bin_mdef_pid2tmatid(m,p):
    return ((m).phone[p].tmat)
def bin_mdef_silphone(m):
    return ((m).sil)
def bin_mdef_sen2cimap(m,s):
    return ((m).sen2cimap[s])
def bin_mdef_sseq2sen(m,ss,pos):
    return ((m).sseq[ss][pos])
def bin_mdef_pid2ci(m,p):
    return (((p) < (m).n_ciphone) if (p) else (m).phone[p].info.cd.ctx[0])
NULL = 0

# <------------------------------------------------------------------------------------------------------------------->
# <------------------------------------------------------------------------------------------------------------------->
# <------------------------------------------- (bin_mdef.c) ---------------------------------------------------------->
# <------------------------------------------------------------------------------------------------------------------->
# <------------------------------------------------------------------------------------------------------------------->
'''/* -*- c-basic-offset: 4; indent-tabs-mode: nil -*- */
/* ====================================================================
 * Copyright (c) 2005 Carnegie Mellon University.  All rights 
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
/*********************************************************************
 *
 * File: bin_mdef.c
 * 
 * Description: 
 *	Binary format model definition files, with support for
 *	heterogeneous topologies and variable-size N-phones
 *
 * Author: 
 * 	David Huggins-Daines <dhdaines@gmail.com>
 *********************************************************************/
'''
#include <stdio.h>
#include <string.h>
#include <assert.h>

#include <pocketsphinx.h>

#include "util/ckd_alloc.h"
#include "util/byteorder.h"
#include "util/case.h"
#include "mdef.h"
#include "bin_mdef.h"

def bin_mdef_read_text(config, filename):
    
    if ((mdef := mdef.mdef_init(filename, True)) == NULL):
        return NULL
    
    #3 Enforce some limits.  */
    if (mdef.n_sen > BAD_SENID):
        mdef.mdef_free(mdef)
        return NULL
    if (mdef.n_sseq > BAD_SSID):
        mdef.mdef_free(mdef)
        return NULL
    
    # We use uint8 for ciphones */
    if (mdef.n_ciphone > 255):
        mdef.mdef_free(mdef)
        return NULL
    
    
    bmdef = ckd_alloc.ckd_calloc(1, len(bmdef))
    bmdef.refcnt = 1
    
    # Easy stuff.  The mdef.c code has done the heavy lifting for us. */
    bmdef.n_ciphone = mdef.n_ciphone
    bmdef.n_phone = mdef.n_phone
    bmdef.n_emit_state = mdef.n_emit_state
    bmdef.n_ci_sen = mdef.n_ci_sen
    bmdef.n_sen = mdef.n_sen
    bmdef.n_tmat = mdef.n_tmat
    bmdef.n_sseq = mdef.n_sseq
    bmdef.sseq = mdef.sseq
    bmdef.cd2cisen = mdef.cd2cisen
    bmdef.sen2cimap = mdef.sen2cimap
    bmdef.n_ctx = 3           #/* Triphones only. */
    bmdef.sil = mdef.sil
    mdef.sseq = NULL        #/* We are taking over this one. */
    mdef.cd2cisen = NULL      #/* And this one. */
    mdef.sen2cimap = NULL     #/* And this one. */

    ''' Get the phone names.  If they are not sorted
     * ASCII-betically then we are in a world of hurt and
     * therefore will simply refuse to continue. */'''
    bmdef.ciname = ckd_alloc.ckd_calloc(bmdef.n_ciphone, len(bmdef.ciname))
    nchars = 0
    for i in range(0 , bmdef.n_ciphone):
        nchars += len(mdef.ciphone[i].name) + 1
    bmdef.ciname[0] = ckd_alloc.ckd_calloc(nchars, 1)
    for i in range(0 , bmdef.n_ciphone):
        assert(i > 0);    # /* No reason to imagine it wouldn't be, but... */
        bmdef.ciname[i] = bmdef.ciname[i - 1] + len(bmdef.ciname[i - 1]) + 1
        if (bmdef.ciname[i - 1] > bmdef.ciname[i]):
            # /* FIXME: there should be a solution to this, actually. */
            err.E_ERROR("Phone names are not in sorted order, sorry.")
            bin_mdef_free(bmdef)
            return NULL
    
    # Copy over phone information. */
    bmdef.phone = ckd_alloc.ckd_calloc(bmdef.n_phone, len(bmdef.phone))
    for i in range(0 , mdef.n_phone):
        bmdef.phone[i].ssid = mdef.phone[i].ssid
        bmdef.phone[i].tmat = mdef.phone[i].tmat
        if (i < bmdef.n_ciphone):
            bmdef.phone[i].info.ci.filler = mdef.ciphone[i].filler
        
        else:
            bmdef.phone[i].info.cd.wpos = mdef.phone[i].wpos
            bmdef.phone[i].info.cd.ctx[0] = mdef.phone[i].ci
            bmdef.phone[i].info.cd.ctx[1] = mdef.phone[i].lc
            bmdef.phone[i].info.cd.ctx[2] = mdef.phone[i].rc
    
    ''' Walk the wpos_ci_lclist once to find the total number of
     * nodes and the starting locations for each level. */'''
    nodes = lc_idx = ci_idx = rc_idx = 0
    for i in range(0 , bin_mdef_t.N_WORD_POSN):
        
        for j in range(0 , mdef.n_ciphone):
            
            lc = mdef.wpos_ci_lclist[i][j]
            while(lc):
                rc = lc.rclist
                while (rc):
                    nodes += 1    # /* RC node */
                    rc = rc.next
                
                nodes += 1        #   /* LC node */
                rc_idx += 1       #   /* Start of RC nodes (after LC nodes) */
                lc.next
            
            nodes += 1            # /* CI node */
            lc_idx += 1           # /* Start of LC nodes (after CI nodes) */
            rc_idx += 1           # /* Start of RC nodes (after CI and LC nodes) */
        
        nodes += 1                # /* wpos node */
        ci_idx += 1;              # /* Start of CI nodes (after wpos nodes) */
        lc_idx += 1               # /* Start of LC nodes (after CI nodes) */
        rc_idx += 1               # /* STart of RC nodes (after wpos, CI, and LC nodes) */
    
    bmdef.n_cd_tree = nodes
    bmdef.cd_tree = ckd_alloc.ckd_calloc(nodes, len(bmdef.cd_tree))
    for i in range(0 , bin_mdef_t.N_WORD_POSN):
        
        bmdef.cd_tree[i].ctx = i
        bmdef.cd_tree[i].n_down = mdef.n_ciphone
        bmdef.cd_tree[i].c.down = ci_idx
        
        # Now we can build the rest of the tree. */
        for j in range(0 , mdef.n_ciphone):
            
            bmdef.cd_tree[ci_idx].ctx = j
            bmdef.cd_tree[ci_idx].c.down = lc_idx
            lc = mdef.wpos_ci_lclist[i][j]
            while(lc):
                
                bmdef.cd_tree[lc_idx].ctx = lc.lc
                bmdef.cd_tree[lc_idx].c.down = rc_idx
                rc = lc.rclist
                while (rc):
                    bmdef.cd_tree[rc_idx].ctx = rc.rc
                    bmdef.cd_tree[rc_idx].n_down = 0
                    bmdef.cd_tree[rc_idx].c.pid = rc.pid
                    
                    bmdef.cd_tree[lc_idx].n_down += 1
                    rc_idx += 1
                    rc = rc.next
                
                '''If there are no triphones here,
                 * this is considered a leafnode, so
                 * set the pid to -1. */ '''
                if (bmdef.cd_tree[lc_idx].n_down == 0):
                    bmdef.cd_tree[lc_idx].c.pid = -1
                
                bmdef.cd_tree[ci_idx].n_down
                lc_idx += 1
                lc = lc.next
            
            
            # As above, so below. */
            if (bmdef.cd_tree[ci_idx].n_down == 0):
                bmdef.cd_tree[ci_idx].c.pid = -1
            
            
            ci_idx += 1
    
    bmdef.alloc_mode = bin_mdef_t.BIN_MDEF_FROM_TEXT
    return bmdef


def bin_mdef_retain(m):
    m.refcnt += 1
    return m


def bin_mdef_free(m):
    if (m == NULL):
        return 0
    if (m.refcnt > 0):
        m.refcnt -= 1
        return m.refcnt
    
    if(m.alloc_mode == bin_mdef_t.BIN_MDEF_FROM_TEXT):
        ckd_alloc.ckd_free(m.ciname[0])
        ckd_alloc.ckd_free(m.sseq[0])
        ckd_alloc.ckd_free(m.phone)
        ckd_alloc.ckd_free(m.cd_tree)
    
    if(m.alloc_mode == BIN_MDEF_IN_MEMORY):
        ckd_alloc.ckd_free(m.ciname[0])
    
    if (m.filemap):
        mmio.mmio_file_unmap(m.filemap)
    ckd_alloc.ckd_free(m.cd2cisen)
    ckd_alloc.ckd_free(m.sen2cimap)
    ckd_alloc.ckd_free(m.ciname)
    ckd_alloc.ckd_free(m.sseq)
    ckd_alloc.ckd_free(m)
    return 0


format_desc = [
    "BEGIN FILE FORMAT DESCRIPTION\n"
    "int32 n_ciphone;    /**< Number of base (CI) phones */\n"
    "int32 n_phone;	     /**< Number of base (CI) phones + (CD) triphones */\n"
    "int32 n_emit_state; /**< Number of emitting states per phone (0 if heterogeneous) */\n"
    "int32 n_ci_sen;     /**< Number of CI senones; these are the first */\n"
    "int32 n_sen;	     /**< Number of senones (CI+CD) */\n"
    "int32 n_tmat;	     /**< Number of transition matrices */\n"
    "int32 n_sseq;       /**< Number of unique senone sequences */\n"
    "int32 n_ctx;	     /**< Number of phones of context */\n"
    "int32 n_cd_tree;    /**< Number of nodes in CD tree structure */\n"
    "int32 sil;	     /**< CI phone ID for silence */\n"
    "char ciphones[][];  /**< CI phone strings (null-terminated) */\n"
    "char padding[];     /**< Padding to a 4-bytes boundary */\n"
    "struct { int16 ctx; int16 n_down; int32 pid/down } cd_tree[];\n"
    "struct { int32 ssid; int32 tmat; int8 attr[4] } phones[];\n"
    "int16 sseq[];       /**< Unique senone sequences */\n"
    "int8 sseq_len[];    /**< Number of states in each sseq (none if homogeneous) */\n"
    "END FILE FORMAT DESCRIPTION\n" ]


def bin_mdef_write(m, filename):
    
    # Byteorder marker. */
    
    # Round the format descriptor size up to a 4-byte boundary. */
    val = ((len(format_desc) + 3) & ~3)
    # Phone strings. */
    for i in range(0 , m.ciphone):
        continue
    i = 0
    if (m.n_emit_state):
        # Write size of sseq */
        val = m.n_sseq * m.n_emit_state
    
    else:
        
        # Calculate size of sseq */
        n = 0
        for i in range(0 , m.n_sseq):
            n += m.sseq_len[i]
    
    return 0


def bin_mdef_write_text(m, filename):
    if (filename == "-"):
        fh = 'stdout'
    
    if (m.n_emit_state):
        n_total_state = m.n_phone * (m.n_emit_state + 1)
    else:
        n_total_state = 0
        for i in range(0 ,  m.n_phone):
            n_total_state += m.sseq_len[m.phone[i].ssid] + 1
    
    for p in range(0 , m.n_ciphone):
        if (m.n_emit_state):
            n_state = m.n_emit_state
        else:
            n_state = m.sseq_len[m.phone[p].ssid]
    
    for p in range(0 , m.n_ciphone):
        if (m.n_emit_state):
            n_state = m.n_emit_state
        else:
            n_state = m.sseq_len[m.phone[p].ssid]
        for i in range(0 , n_state):
            continue
    return 0


def bin_mdef_ciphone_id(m, ciphone):
    # Exact binary search on m->ciphone */
    low = 0
    high = m.n_ciphone
    while (low < high):
        mid = (low + high) / 2
        c = (ciphone == m.ciname[mid])
        if (c == 0):
            return mid
        elif (c > 0):
            low = mid + 1
        else:
            high = mid
    
    return -1



def bin_mdef_ciphone_id_nocase(m, ciphone):
    
    # Exact binary search on m->ciphone */
    low = 0
    high = m.n_ciphone
    while (low < high):
        
        mid = (low + high) / 2
        c = (ciphone == m.ciname[mid])
        if (c == 0):
            return mid
        elif (c > 0):
            low = mid + 1
        else:
            high = mid
    
    return -1


def bin_mdef_ciphone_str(m, ci):
    assert(m != NULL)
    assert(ci < m.n_ciphone)
    return m.ciname[ci]


def bin_mdef_phone_id(m, ci, lc, rc, wpos):
    
    assert(m)
    ctx = []
    ''' In the future, we might back off when context is not available,
     * but for now we'll just return the CI phone. '''
    if (lc < 0 or rc < 0):
        return ci
    
    assert((ci >= 0) and (ci < m.n_ciphone))
    assert((lc >= 0) and (lc < m.n_ciphone))
    assert((rc >= 0) and (rc < m.n_ciphone))
    assert((wpos >= 0) and (wpos < bin_mdef_t.N_WORD_POSN))
    
    # Create a context list, mapping fillers to silence. */
    ctx[0] = wpos
    ctx[1] = ci
    ctx[2] = (m.sil >= 0 and m.phone[lc].info.ci.filler) if m.sil else lc
    ctx[3] = (m.sil >= 0 and m.phone[rc].info.ci.filler) if m.sil else rc
    
    # Walk down the cd_tree. */
    cd_tree = m.cd_tree
    level = 0                   # /* What level we are on. */
    max = N_WORD_POSN           # /* Number of nodes on this level. */
    
    while (level < 4):
        for i in range(0 , max):
            
            if (cd_tree[i].ctx == ctx[level]):
                break
        
        if (i == max):
            return -1
        
        # Leaf node, stop here. */
        if (cd_tree[i].n_down == 0):
            return cd_tree[i].c.pid
        
        # Go down one level. */
        max = cd_tree[i].n_down
        cd_tree = m.cd_tree + cd_tree[i].c.down
        level += 1
    
    # We probably shouldn't get here. */
    return -1


def bin_mdef_phone_id_nearest(m, b, l, r, pos):
    
    # In the future, we might back off when context is not available,
    #  but for now we'll just return the CI phone. */
    if (l < 0 or r < 0):
        return b
    
    p = bin_mdef_phone_id(m, b, l, r, pos)
    if (p >= 0):
        return p
    
    # Exact triphone not found; backoff to other word positions */
    for tmppos in range(0 , N_WORD_POSN):
        if (tmppos != pos):
            p = bin_mdef_phone_id(m, b, l, r, tmppos)
            if (p >= 0):
                return p
    
    
    # Nothing yet; backoff to silence phone if non-silence filler context */
    # In addition, backoff to silence phone on left/right if in beginning/end position */
    if (m.sil >= 0):
        newl = l
        newr = r
        if (m.phone[l].info.ci.filler):
            newl = m.sil
        if (m.phone[r].info.ci.filler):
            newr = m.sil
        if ((newl != l) or (newr != r)):
            p = bin_mdef_phone_id(m, b, newl, newr, pos)
            if (p >= 0):
                return p
            
            for tmppos in range(0 , N_WORD_POSN):
                if (tmppos != pos):
                    p = bin_mdef_phone_id(m, b, newl, newr, tmppos)
                    if (p >= 0):
                        return p
    
    
    # Nothing yet; backoff to base phone */
    return b


def bin_mdef_phone_str(m, pid, buf):
    assert(m)
    assert((pid >= 0) and (pid < m.n_phone))
    buf[0] = '\0'
    return 0

