import ps_config
import mmio
import logmath
import acmod
import dict
import err
import bin_mdef
import strfuncs
import ckd_alloc

NULL = 0
# <------------------------------------------------------------------------------------------------------------------->
# <------------------------------------------------------------------------------------------------------------------->
# <----------------------------------------------------- dict.h() ---------------------------------------------------->
# <------------------------------------------------------------------------------------------------------------------->
# <------------------------------------------------------------------------------------------------------------------->

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

#ifndef _S3_DICT_H_
#define _S3_DICT_H_

/** \file dict.h
 * \brief Operations on dictionary. 
 */

#include <pocketsphinx.h>

#include "s3types.h"
#include "bin_mdef.h"
#include "util/hash_table.h"
#include "pocketsphinx/export.h"

#define S3DICT_INC_SZ 4096

#ifdef __cplusplus
extern "C" {
#endif
#if 0
}
#endif
'''
'''
    \struct dictword_t
    \brief a structure for one dictionary word. 
*/
typedef struct dictword_s {   } dictword_t;  '''
class dictword_s:
    word = ''                  # char *word;		/**< Ascii word string */
    ciphone = s3cipid_t()      # s3cipid_t *ciphone;	/**< Pronunciation */
    pronlen = 0                # int32 pronlen;	/**< Pronunciation length */
    alt = s3wid_t()            # s3wid_t alt;	/**< Next alternative pronunciation id, NOT_S3WID if none */
    basewid = s3wid_t()        # s3wid_t basewid;	/**< Base pronunciation id */
dictword_t = dictword_s


'''
\struct dict_t
\brief a structure for a dictionary. 
typedef struct dict_s {   } dict_t;
'''
class dict_s:
    refcnt = 0             # int refcnt
    mdef = bin_mdef.bin_mdef_t()    # bin_mdef_t *mdef;	   # /**< Model definition used for phone IDs; NULL if none used */
    word = dictword_t()    # dictword_t *word;	   # /**< Array of entries in dictionary */
    ht = ps_config.hash_table_t # hash_table_t *ht;	   # /**< Hash table for mapping word strings to word ids */
    max_words = 0          # int32 max_words;	   # /**< #Entries allocated in dict, including empty slots */
    n_word = 0             # int32 n_word;	       # /**< #Occupied entries in dict; ie, excluding empty slots */
    filler_start = 0       # int32 filler_start;	   # /**< First filler word id (read from filler dict) */
    filler_end = 0         # int32 filler_end;	   # /**< Last filler word id (read from filler dict) */
    startwid = s3wid_t()   # s3wid_t startwid;	   # /**< FOR INTERNAL-USE ONLY */
    finishwid = s3wid_t()  # s3wid_t finishwid;	   # /**< FOR INTERNAL-USE ONLY */
    silwid = s3wid_t()     # s3wid_t silwid;	       # /**< FOR INTERNAL-USE ONLY */
    nocase = 0             # int nocase
dict_t = dict_s


#  Packaged macro access to dictionary members */
def dict_size(d):
    return d.n_word
def dict_num_fillers(d):
    return (dict_filler_end(d) - dict_filler_start(d))

'''
 * Number of "real words" in the dictionary.
 *
 * This is the number of words that are not fillers, <s>, or </s>.
 */
'''

def dict_num_real_words(d):                                          
    return (dict_size(d) - (dict_filler_end(d) - dict_filler_start(d)) - 2)
def dict_basewid(d,w):
    return (d.word[w].basewid)
def dict_wordstr(d,w):
    return (NULL if w < 0 else d.word[w].word)
def dict_basestr(d,w):
    return (d.word[dict_basewid(d,w)].word)
def dict_nextalt(d,w):
    return (d.word[w].alt)
def dict_pronlen(d,w):
    (d.word[w].pronlen) 
def dict_pron(d,w,p):
    return (d.word[w].ciphone[p])       # /**< The CI phones of the word w at position p */
def dict_filler_start(d):
    return (d.filler_start)
def dict_filler_end(d):
    return (d.filler_end)
def dict_startwid(d):
    return (d.startwid)
def dict_finishwid(d):
    return (d.finishwid)
def dict_silwid(d):
    return (d.silwid)
def dict_is_single_phone(d,w):
    return (d.word[w].pronlen == 1)
def dict_first_phone(d,w):
    return (d.word[w].ciphone[0])
def dict_second_phone(d,w):
    return (d.word[w].ciphone[1])
def dict_second_last_phone(d,w):
    return (d.word[w].ciphone[d.word[w].pronlen - 2])
def dict_last_phone(d,w):
    return (d.word[w].ciphone[d.word[w].pronlen - 1])

# Hard-coded special words */
S3_START_WORD = "<s>"
S3_FINISH_WORD = "</s>"
S3_SILENCE_WORD = "<sil>"
S3_UNKNOWN_WORD = "<UNK>"

# <------------------------------------------------------------------------------------------------------------------->
# <------------------------------------------------------------------------------------------------------------------->
# <----------------------------------------------------- dict.c() ---------------------------------------------------->
# <------------------------------------------------------------------------------------------------------------------->
# <------------------------------------------------------------------------------------------------------------------->
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
#include <string.h>

#include "util/pio.h"
#include "util/ckd_alloc.h"
#include "util/strfuncs.h"
#include "dict.h"

DELIM = " \t\n"         # Set of field separator characters */
DEFAULT_NUM_PHONE = (MAX_S3CIPID+1)

# static s3cipid_t dict_ciphone_id(dict_t * d, const char *str)
def dict_ciphone_id(d, stri):
    if (d.nocase):
        return bin_mdef.bin_mdef_ciphone_id_nocase(d.mdef, stri)
    else:
        return bin_mdef.bin_mdef_ciphone_id(d.mdef, stri)



'''
 * Return value: CI phone string for the given word, phone position.
 */
const char *dict_ciphone_str(dict_t *d,	/**< In: Dictionary to look up */
                             s3wid_t wid,	/**< In: Component word being looked up */
                             int32 pos   	/**< In: Pronunciation phone position */
    );  '''

def dict_ciphone_str(d, wid, pos):
    assert(d != NULL)
    assert((wid >= 0) and (wid < d.n_word))
    assert((pos >= 0) and (pos < d.word[wid].pronlen))
    return bin_mdef_ciphone_str(d.mdef, d.word[wid].ciphone[pos])



'''
 * Add a word with the given ciphone pronunciation list to the dictionary.
 * Return value: Result word id if successful, BAD_S3WID otherwise
 */
s3wid_t dict_add_word(dict_t *d,          /**< The dictionary structure. */
                      char const *word,   /**< The word. */
                      s3cipid_t const *p, /**< The pronunciation. */
                      int32 np            /**< Number of phones. */
    );  '''
def dict_add_word(d, word, p, np):
    # int32 len;
    wordp = dictword_t()   # dictword_t *wordp;
    newwid = s3wid_t()     # s3wid_t newwid;
    wword = ''
    
    if (d.n_word >= d.max_words):
        # E_INFO("Reallocating to %d KiB for word entries\n", (d.max_words + S3DICT_INC_SZ) * sizeof(dictword_t) / 1024)
        # d.word = (dictword_t *) ckd_realloc(d.word, (d.max_words + S3DICT_INC_SZ) * sizeof(dictword_t))
        d.max_words = d.max_words + S3DICT_INC_SZ
    
    
    wordp = d.word + d.n_word
    # wordp.word = (char *) ckd_salloc(word);    /* Freed in dict_free */
    
    # Determine base/alt wids */
    # wword = ckd_salloc(word);
    if ((len := dict_word2basestr(wword)) > 0):
        # int32 w;
        
        # Truncated to a baseword string; find its ID */
        if (ps_config.hash_table_lookup_int32(d.ht, wword, w) < 0):
            err.E_ERROR("Missing base word for: %s\n", word)
            ckd_alloc.ckd_free(wword)
            ckd_alloc.ckd_free(wordp.word)
            wordp.word = NULL
            return BAD_S3WID
        
        
        # Link into alt list */
        wordp.basewid = w
        wordp.alt = d.word[w].alt
        d.word[w].alt = d.n_word
    
    else: 
        wordp.alt = BAD_S3WID
        wordp.basewid = d.n_word
    # ckd_free(wword);
    
    # Associate word string with d->n_word in hash table */
    if (ps_config.hash_table_enter_int32(d.ht, wordp.word, d.n_word) != d.n_word): 
        # ckd_free(wordp->word)
        wordp.word = NULL
        return BAD_S3WID
    
    
    # Fill in word entry, and set defaults */
    if (p and (np > 0)):
        # wordp.ciphone = ckd_malloc(np * sizeof(s3cipid_t));      # Freed in dict_free */
        p = wordp.ciphone # memcpy(wordp.ciphone, p, np * sizeof(s3cipid_t))
        wordp.pronlen = np
    
    else:
        wordp.ciphone = NULL
        wordp.pronlen = 0
    
    newwid = d.n_word + 1
    return newwid


# static int32 dict_read(FILE * fp, dict_t * d)
def dict_read(fp, d):
    # lineiter_t *li;
    # char **wptr;
    # s3cipid_t *p;
    # int32 lineno, nwd;
    # s3wid_t w;
    # int32 i, maxwd;
    # size_t stralloc, phnalloc;
    
    maxwd = 512
    # p = (s3cipid_t *) ckd_calloc(maxwd + 4, sizeof(*p));
    # wptr = (char **) ckd_calloc(maxwd, sizeof(char *)); /* Freed below */
    
    lineno = 0
    stralloc = phnalloc = 0
    # for (li = lineiter_start(fp); li; li = lineiter_next(li))
    li = strfuncs.lineiter_start(fp)
    while(li):
        lineno += 1
        if ((li.buf == "##", 2) or 0 == li.buf == ";;"):
            continue
        
        if ((nwd := strfuncs.str2words(li.buf, wptr, maxwd)) < 0):
            # Increase size of p, wptr. */
            nwd = strfuncs.str2words(li.buf, NULL, 0)
            assert(nwd > maxwd);  #  why else would it fail? */
            maxwd = nwd
            # p = (s3cipid_t *) ckd_realloc(p, (maxwd + 4) * sizeof(*p));
            # wptr = (char **) ckd_realloc(wptr, maxwd * sizeof(*wptr));
        
        
        if (nwd == 0):           # Empty line 
            continue
        # wptr[0] is the word-string and wptr[1..nwd-1] the pronunciation sequence */
        if (nwd == 1):
            err.E_ERROR("Line %d: No pronunciation for word '%s'; ignored\n", lineno, wptr[0])
            continue
        
        
        
        # Convert pronunciation string to CI-phone-ids */
        # for (i = 1; i < nwd; i++) {
        for i in range(1 , nwd):
            p[i - 1] = dict_ciphone_id(d, wptr[i])
            if (NOT_S3CIPID(p[i - 1])):
                err.E_ERROR("Line %d: Phone '%s' is missing in the acoustic model; word '%s' ignored\n", lineno, wptr[i], wptr[0])
                break
        
        
        
        if (i == nwd):          # /* All CI-phones successfully converted to IDs */
            w = dict_add_word(d, wptr[0], p, nwd - 1)
            if (NOT_S3WID(w)):
                # E_ERROR ("Line %d: Failed to add the word '%s' (duplicate?); ignored\n", lineno, wptr[0])
                continue
            else:
                stralloc += len(d.word[w].word)
                phnalloc += d.word[w].pronlen * len(s3cipid_t)
        
        
        li = strfuncs.lineiter_next(li)
    #E_INFO("Dictionary size %d, allocated %d KiB for strings, %d KiB for phones\n", dict_size(d), (int)stralloc / 1024, (int)phnalloc / 1024);
    #ckd_free(p);
    #ckd_free(wptr);
    
    return 0


'''
 * Write dictionary to a file.
 */
int dict_write(dict_t *dict, char const *filename, char const *format);  '''

def dict_write(dict, filename, format):
    #FILE *fh;
    #int i;
    
    #(void)format; /* FIXME */
    if ((fh := fopen(filename, "w")) == NULL):
        # E_ERROR_SYSTEM("Failed to open '%s'", filename)
        return -1
    
    # for (i = 0; i < dict->n_word; ++i) {
    for i in range(0 , dict.n_word):
        # char *phones
        # int j, phlen
        if (dict_real_word(dict, i) != NULL):
            continue
        # for (phlen = j = 0; j < dict_pronlen(dict, i); ++j)
        phlen = 0
        for j in range(0 , dict_pronlen(dict, i)):
            phlen += len(dict_ciphone_str(dict, i, j)) + 1
        # phones = ckd_calloc(1, phlen)
        # for (j = 0; j < dict_pronlen(dict, i); ++j):
        for j in range(0 , dict_pronlen(dict, i)):
            phones = phones + dict_ciphone_str(dict, i, j) # strcat(phones, dict_ciphone_str(dict, i, j))
            if (j != dict_pronlen(dict, i) - 1):
                phones = phones + " " # strcat(phones, " ")
    return 0



'''
 * Initialize a new dictionary.
 *
 * If config and mdef are supplied, then the dictionary will be read
 * from the files specified by the -dict and -fdict options in config,
 * with case sensitivity determined by the -dictcase option.
 *
 * Otherwise an empty case-sensitive dictionary will be created.
 *
 * Return ptr to dict_t if successful, NULL otherwise.
 */
dict_t *dict_init(ps_config_t *config, /**< Configuration (-dict, -fdict, -dictcase) or NULL */
                  bin_mdef_t *mdef  /**< For looking up CI phone IDs (or NULL) */
    );  '''
def dict_init(config, mdef):
    fp = FILE() # FILE *fp, *fp2;
    fp2 = FILE() 
    # int32 n;
    li = lineiter_t()    # lineiter_t *li;
    d = dict_t()         # dict_t *d;
    sil = s3cipid_t()    # s3cipid_t sil;
    dictfile = NULL      # char const *dictfile = NULL, *fillerfile = NULL;
    fillerfile = NULL
    
    if(config):
        dictfile = ps_config.ps_config_str(config, "dict")
        fillerfile = ps_config.ps_config_str(config, "fdict")
    
    
    '''
     * First obtain #words in dictionary (for hash table allocation).
     * Reason: The PC NT system doesn't like to grow memory gradually.  Better to allocate
     * all the required memory in one go.
    '''
    fp = NULL
    n = 0
    if (dictfile):
        if ((fp := fopen(dictfile, "r")) == NULL):
            # E_ERROR_SYSTEM("Failed to open dictionary file '%s' for reading", dictfile)
            return NULL
        
        # for (li = lineiter_start(fp); li; li = lineiter_next(li)):
        li = strfuncs.lineiter_start(fp)
        while(li):
            if ((li.buf != "##", 2) and (li.buf !=";;")):
                n += 1
            li = strfuncs.lineiter_next(li)

    
    
    fp2 = NULL
    if (fillerfile):
        if ((fp2 := fopen(fillerfile, "r")) == NULL):
            err.E_ERROR_SYSTEM("Failed to open filler dictionary file '%s' for reading", fillerfile)
            return NULL
        
        # for (li = lineiter_start(fp2); li; li = lineiter_next(li)) {
        li = strfuncs.lineiter_start(fp2)
        while(li):
            if ((li.buf != "##") and (li.buf != ";;")):
                n += 1
            li = strfuncs.lineiter_next(li)
    
    
    '''
     * Allocate dict entries.  HACK!!  Allow some extra entries for words not in file.
     * Also check for type size restrictions.
    '''
    # d = (dict_t *) ckd_calloc(1, sizeof(dict_t));       /* freed in dict_free() */
    d.refcnt = 1
    d.max_words = n + S3DICT_INC_SZ if (n + S3DICT_INC_SZ < MAX_S3WID) else MAX_S3WID
    if (n >= MAX_S3WID):
        err.E_ERROR("Number of words in dictionaries (%d) exceeds limit (%d)\n", n, MAX_S3WID)
        ckd_alloc.ckd_free(d)
        return NULL
    
    
    err.E_INFO("Allocating %d * %d bytes (%d KiB) for word entries\n", d.max_words, len(dictword_t), d.max_words * len(dictword_t) / 1024)
    # d->word = (dictword_t *) ckd_calloc(d->max_words, sizeof(dictword_t));      /* freed in dict_free() */
    d.n_word = 0
    if (mdef):
        d.mdef = bin_mdef.bin_mdef_retain(mdef)
    
    # Create new hash table for word strings; case-insensitive word strings */
    if (config):
        d.nocase = ps_config.ps_config_bool(config, "dictcase")
    d.ht = ps_config.hash_table_new(d.max_words, d.nocase)
    
    # Digest main dictionary file */
    if (fp):
        err.E_INFO("Reading main dictionary: %s\n", dictfile)
        dict_read(fp, d)
        err.E_INFO("%d words read\n", d.n_word)
    
    
    if (dict_wordid(d, S3_START_WORD) != BAD_S3WID):
        err.E_ERROR("Remove sentence start word '<s>' from the dictionary\n")
        dict_free(d)
        return NULL
    
    if (dict_wordid(d, S3_FINISH_WORD) != BAD_S3WID):
        err.E_ERROR("Remove sentence start word '</s>' from the dictionary\n")
        dict_free(d)
        return NULL
    
    if (dict_wordid(d, S3_SILENCE_WORD) != BAD_S3WID):
        err.E_ERROR("Remove silence word '<sil>' from the dictionary\n")
        dict_free(d)
        return NULL
    
    
    # Now the filler dictionary file, if it exists */
    d.filler_start = d.n_word
    if (fp2):
        err.E_INFO("Reading filler dictionary: %s\n", fillerfile)
        dict_read(fp2, d)
        err.E_INFO("%d words read\n", d.n_word - d.filler_start)
    
    if (mdef):
        sil = bin_mdef.bin_mdef_silphone(mdef)
    else:
        sil = 0
    if (dict_wordid(d, S3_START_WORD) == BAD_S3WID):
        dict_add_word(d, S3_START_WORD, sil, 1)
    
    if (dict_wordid(d, S3_FINISH_WORD) == BAD_S3WID):
        dict_add_word(d, S3_FINISH_WORD, sil, 1)
    
    if (dict_wordid(d, S3_SILENCE_WORD) == BAD_S3WID):
        dict_add_word(d, S3_SILENCE_WORD, sil, 1)
    
    
    d.filler_end = d.n_word - 1
    
    # Initialize distinguished word-ids */
    d.startwid = dict_wordid(d, S3_START_WORD)
    d.finishwid = dict_wordid(d, S3_FINISH_WORD)
    d.silwid = dict_wordid(d, S3_SILENCE_WORD)
    
    if ((d.filler_start > d.filler_end) or (dict_filler_word(d, d.silwid) != NULL)):
        err.E_ERROR("Word '%s' must occur (only) in filler dictionary\n",  S3_SILENCE_WORD)
        dict_free(d)
        return NULL
    
    # No check that alternative pronunciations for filler words are in filler range!! */
    return d


'''
# Return word id for given word string if present.  Otherwise return BAD_S3WID */
# POCKETSPHINX_EXPORT
s3wid_t dict_wordid(dict_t *d, const char *word); '''

def dict_wordid(d, word):
    w = 0
    
    assert(d)
    assert(word)
    
    if (ps_config.hash_table_lookup_int32(d.ht, word, w) < 0):
        return (BAD_S3WID)
    return w



'''
 * Return 1 if w is a filler word, 0 if not.  A filler word is one that was read in from the
 * filler dictionary; however, sentence START and FINISH words are not filler words.
 */
int dict_filler_word(dict_t *d,  /**< The dictionary structure */
                     s3wid_t w     /**< The word ID */
    );  '''

def dict_filler_word(d, w):
    assert(d)
    assert((w >= 0) and(w < d.n_word))
    
    w = dict_basewid(d, w)
    if ((w == d.startwid) or (w == d.finishwid)):
        return 0
    if ((w >= d.filler_start) and (w <= d.filler_end)):
        return 1
    return 0


'''
 * Test if w is a "real" word, i.e. neither a filler word nor START/FINISH.
 */
POCKETSPHINX_EXPORT
int dict_real_word(dict_t *d,  /**< The dictionary structure */
                   s3wid_t w     /**< The word ID */
    );  '''
def dict_real_word(d, w):
    assert(d)
    assert((w >= 0) and (w < d.n_word))
    
    w = dict_basewid(d, w)
    if ((w == d.startwid) or (w == d.finishwid)):
        return 0
    if ((w >= d.filler_start) and (w <= d.filler_end)):
        return 0
    return 1



'''
 * If the given word contains a trailing "(....)" (i.e., a Sphinx-II style alternative
 * pronunciation specification), strip that trailing portion from it.  Note that the given
 * string is modified.
 * Return value: If string was modified, the character position at which the original string
 * was truncated; otherwise -1.
 */
int32 dict_word2basestr(char *word);  '''

def dict_word2basestr(word):
    # int32 i, len;

    len = len(word)
    if (word[len - 1] == ')'):
        # for (i = len - 2; (i > 0) and (word[i] != '('); --i);
        i = len - 2
        while ((i > 0) and (word[i] != '(')):
            # The word is of the form <baseword>(...); strip from left-paren */
            word[i] = '\0'
            return i
    return -1

'''
 * Retain a pointer to an dict_t.
 */
dict_t *dict_retain(dict_t *d);  '''
def dict_retain(d):
    d.refcnt += 1
    return d


# <---------------------------------------- dict_free() ------------------------------------------->
# Release a pointer to a dictionary.
# int dict_free(dict_t * d){
def dict_free(d):
    # int i;
    word = dict.dictword_t()  # dictword_t *word;
    
    if (d == NULL):
        return 0
    d.refcnt =- 1
    if (d.refcnt > 0):
        return d.refcnt
    
    # First Step, free all memory allocated for each word */
    for i in range(0 , d.n_word):   # for (i = 0; i < d->n_word; i++)
        # word = (dictword_t *) & (d->word[i]);
        if (d.word[i].word):              # if (word->word)
            word[i].word = None                  # ckd_free((void *) word->word);
        if (d.word[i].ciphone):           # if (word->ciphone)
            d.word[i].ciphone = None             # ckd_free((void *) word->ciphone);
    
    if (d.word[i]):                # if (d->word)
        d.word[i] = None           # ckd_free((void *) d->word);
    if (d.ht):
        ps_config.hash_table_free(d.ht)
    if (d.mdef):
        # bin_mdef_free(d->mdef);
        l = 0
    # ckd_free((void *) d);
    return 0

def fopen(logfn, wb):
    pass

''' Report a dictionary structure */
void dict_report(dict_t *d /**< A dictionary structure */
    );   '''

def dict_report(d):
    # E_INFO_NOFN("Initialization of dict_t, report:\n")
    # E_INFO_NOFN("Max word: %d\n", d.max_words)
    # E_INFO_NOFN("No of word: %d\n", d.n_word)
    # E_INFO_NOFN("\n")
    
    print("Initialization of dict_t, report:\n")
    print("Max word: %d\n", d.max_words)
    print("No of word: %d\n", d.n_word)
    print("\n")

