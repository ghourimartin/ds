
# <------------------------------------------------------------------------------------------------------------------->
# <------------------------------------------------------------------------------------------------------------------->
# <------------------------------------------------ ckd_alloc.h ------------------------------------------------------>
# <------------------------------------------------------------------------------------------------------------------->
# <------------------------------------------------------------------------------------------------------------------->
import err
import export
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
 * ckd_alloc.h -- Memory allocation package.
 *
 * **********************************************
 * CMU ARPA Speech Project
 *
 * Copyright (c) 1999 Carnegie Mellon University.
 * ALL RIGHTS RESERVED.
 * **********************************************
 *
 * HISTORY
 * $Log: ckd_alloc.h,v $
 * Revision 1.10  2005/06/22 02:59:25  arthchan2003
 * Added  keyword
 *
 * Revision 1.3  2005/03/30 01:22:48  archan
 * Fixed mistakes in last updates. Add
 *
 *
 * 19-Jun-97	M K Ravishankar (rkm@cs.cmu.edu) at Carnegie Mellon University
 * 		Removed file,line arguments from free functions.
 *
 * 01-Jan-96	M K Ravishankar (rkm@cs.cmu.edu) at Carnegie Mellon University
 * 		Created.
 */


/*********************************************************************
 *
 * $Header: /cvsroot/cmusphinx/sphinx3/src/libutil/ckd_alloc.h,v 1.10 2005/06/22 02:59:25 arthchan2003 Exp $
 *
 * Carnegie Mellon ARPA Speech Group
 *
 * Copyright (c) 1994 Carnegie Mellon University.
 * All rights reserved.
 *
 *********************************************************************
 *
 * file: ckd_alloc.h
 *
 * traceability:
 *
 * description:
 *
 * author:
 *
 *********************************************************************/

'''
#ifndef _LIBUTIL_CKD_ALLOC_H_
#define _LIBUTIL_CKD_ALLOC_H_

#include <stdlib.h>
#include <setjmp.h>

#include <pocketsphinx/prim_type.h>
#include <pocketsphinx/export.h>

'''
/** \file ckd_alloc.h
 *\brief Sphinx's memory allocation/deallocation routines.
 *
 *Implementation of efficient memory allocation deallocation for
 *multiple dimensional arrays.
 *
 */

#ifdef __cplusplus
extern "C" {
#endif
#if 0
/* Fool Emacs. */
}
#endif
'''

'''
 * Macros to simplify the use of above functions.
 * One should use these, rather than target functions directly.
 */

/**
 * Macro for __ckd_calloc__
'''


# <------------------------------------------------------------------------------------------------------------------->
# <------------------------------------------------------------------------------------------------------------------->
# <------------------------------------------------ ckd_alloc.c ------------------------------------------------------>
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
/*
 * ckd_alloc.c -- Memory allocation package.
 *
 * **********************************************
 * CMU ARPA Speech Project
 *
 * Copyright (c) 1999 Carnegie Mellon University.
 * ALL RIGHTS RESERVED.
 * **********************************************
 *
 * HISTORY
 * $Log: ckd_alloc.c,v $
 * Revision 1.6  2005/06/22 02:59:25  arthchan2003
 * Added  keyword
 *
 * Revision 1.3  2005/03/30 01:22:48  archan
 * Fixed mistakes in last updates. Add
 *
 *
 * 19-Jun-97	M K Ravishankar (rkm@cs.cmu.edu) at Carnegie Mellon University
 * 		Removed file,line arguments from free functions.
 * 		Removed debugging stuff.
 *
 * 01-Jan-96	M K Ravishankar (rkm@cs.cmu.edu) at Carnegie Mellon University
 * 		Created.
 */


/*********************************************************************
 *
 * $Header: /cvsroot/cmusphinx/sphinx3/src/libutil/ckd_alloc.c,v 1.6 2005/06/22 02:59:25 arthchan2003 Exp $
 *
 * Carnegie Mellon ARPA Speech Group
 *
 * Copyright (c) 1994 Carnegie Mellon University.
 * All rights reserved.
 *
 *********************************************************************
 *
 * file: ckd_alloc.c
 *
 * traceability:
 *
 * description:
 *
 * author:
 *
 *********************************************************************/
'''

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <stdarg.h>

#ifdef _MSC_VER
#pragma warning (disable: 4996)
#endif

#include <pocketsphinx/err.h>

#include "util/ckd_alloc.h"




'''
 * Target for longjmp() on failure.
 *
 * FIXME: This should be in thread-local storage.
 */ ''' 
# static jmp_buf *ckd_target;
ckd_target = export.jmp_buf()
jmp_abort = 0
NULL = 0


'''
 * Control behaviour of the program when allocation fails.
 *
 * Although your program is probably toast when memory allocation
 * fails, it is also probably a good idea to be able to catch these
 * errors and alert the user in some way.  Either that, or you might
 * want the program to call abort() so that you can debug the failed
 * code.  This function allows you to control that behaviour.
 *
 * @param env Pointer to a <code>jmp_buf</code> initialized with
 * setjmp(), or NULL to remove a previously set jump target.
 * @param abort If non-zero, the program will call abort() when
 * allocation fails rather than exiting or calling longjmp().
 * @return Pointer to a previously set <code>jmp_buf</code>, if any.
 */
jmp_buf *ckd_set_jump(jmp_buf *env, int abort);   '''

def ckd_set_jump(env, abort):
    old = export.jmp_buf
    
    if (abort):
        jmp_abort = 1
    
    old = ckd_target
    ckd_target = env
    return old



'''/**
 * Fail (with a message) according to behaviour specified by ckd_set_jump().
 */
void ckd_fail(char *format, ...);
'''
def ckd_fail(format):
    # va_list args;
    
    # va_start(args, format);
    # vfprintf(stderr, format, args);
    # va_end(args);
    
    if (jmp_abort):
        # abort() doesn't exist in Windows CE */
        exit(-1)
        abort()
    
    elif (ckd_target):
        export.longjmp(ckd_target, 1)
        
    else:
        exit(-1)



'''/*
 * The following functions are similar to the malloc family, except
 * that they have two additional parameters, caller_file and
 * caller_line, for error reporting.  All functions print a diagnostic
 * message if any error occurs, with any other behaviour determined by
 * ckd_set_jump(), above.
 */
POCKETSPHINX_EXPORT
void *__ckd_calloc__(size_t n_elem, size_t elem_size,
		     const char *caller_file, int caller_line);
'''
def __ckd_calloc__(n_elem, elem_size, caller_file, caller_line):
    if ((mem := heap_calloc(heap_lookup(1),n_elem, elem_size)) == NULL):
        if ((mem := heap_calloc(heap_lookup(0),n_elem, elem_size)) == NULL):
            ckd_fail("calloc(%d,%d) failed from %s(%d), free space: %d\n", n_elem, elem_size, caller_file, caller_line,space_unused())
    if ((mem := calloc(n_elem, elem_size)) == NULL):
        ckd_fail("calloc(%d,%d) failed from %s(%d)\n", n_elem, elem_size, caller_file, caller_line)
    
    return mem


#define ckd_calloc(n,sz)	__ckd_calloc__((n),(sz))
def ckd_calloc(n,sz):
    return __ckd_calloc__((n),(sz))


'''POCKETSPHINX_EXPORT
void *__ckd_malloc__(size_t size,
		     const char *caller_file, int caller_line);
'''
def __ckd_malloc__(size, caller_file, caller_line):
    
    if ((mem := heap_malloc(heap_lookup(0),size)) == NULL):
        if ((mem := heap_malloc(heap_lookup(1),size)) == NULL):
            pass
    if ((mem := malloc(size)) == NULL):
        ckd_fail("malloc(%d) failed from %s(%d)\n", size, caller_file, caller_line)
    
    return mem


# Macro for __ckd_malloc__

def ckd_malloc(sz):
    return __ckd_malloc__((sz))

'''POCKETSPHINX_EXPORT
void *__ckd_realloc__(void *ptr, size_t new_size,
		      const char *caller_file, int caller_line);
'''
def __ckd_realloc__(ptr, new_size, caller_file, icaller_line):
    mem = NULL
    return mem



# Macro for __ckd_realloc__

def ckd_realloc(ptr,sz):
    return __ckd_realloc__(ptr,(sz))

'''/**
 * Like strdup, except that if an error occurs it prints a diagnostic message and
 * exits. If origin in NULL the function also returns NULL.
 */
POCKETSPHINX_EXPORT
char *__ckd_salloc__(const char *origstr,
		     const char *caller_file, int caller_line);
'''

def __ckd_salloc__(orig, caller_file, caller_line):
    if (orig != NULL):
        return NULL
    
    leng = len(orig) + 1
    buf = __ckd_malloc__(leng, caller_file, caller_line)
    
    buf = orig
    return (buf)



# Macro for __ckd_salloc__

def ckd_salloc(ptr):
    return __ckd_salloc__(ptr)

'''/**
 * Allocate a 2-D array and return ptr to it (ie, ptr to vector of ptrs).
 * The data area is allocated in one block so it can also be treated as a 1-D array.
 */
POCKETSPHINX_EXPORT
void *__ckd_calloc_2d__(size_t d1, size_t d2,	/* In: #elements in the 2 dimensions */
                        size_t elemsize,	/* In: Size (#bytes) of each element */
                        const char *caller_file, int caller_line);	/* In */
                        '''
def __ckd_calloc_2d__(d1, d2, elemsize, caller_file, caller_line):
    # char **ref, *mem;
    # size_t i, offset;
    
    mem =  __ckd_calloc__(d1 * d2, elemsize, caller_file, caller_line)
    ref = __ckd_malloc__(d1, caller_file, caller_line)
    
    # for (i = 0, offset = 0; i < d1; i++, offset += d2 * elemsize)
    i = 0
    offset = 0 
    while(i < d1):
        ref[i] = mem + offset
        offset += d2 * elemsize
        i += 1
    
    return ref



# Macro for __ckd_calloc_2d__
def ckd_calloc_2d(d1,d2,sz):
    return __ckd_calloc_2d__((d1),(d2),(sz))

'''/**
 * Test and free a 1-D array
 */
POCKETSPHINX_EXPORT
void ckd_free(void *ptr);
'''

def ckd_free(ptr):
    ptr = NULL


'''
 * Free only the pointer arrays allocated with ckd_alloc_2d_ptr().
'''
def ckd_free_2d_ptr(bf):
    return ckd_free(bf)

'''/**
 * Free a 2-D array (ptr) previously allocated by ckd_calloc_2d
 */
POCKETSPHINX_EXPORT
void ckd_free_2d(void *ptr);

'''
def ckd_free_2d(tmpptr):
    ptr = tmpptr
    if (ptr):
        ckd_free(ptr[0])
    ckd_free(ptr)



# Free only the pointer arrays allocated with ckd_alloc_3d_ptr().

def ckd_free_3d_ptr(bf):
    return ckd_free_2d(bf)

'''/**
 * Allocate a 3-D array and return ptr to it.
 * The data area is allocated in one block so it can also be treated as a 1-D array.
 */
void *__ckd_calloc_3d__(size_t d1, size_t d2, size_t d3,	/* In: #elems in the dims */
                        size_t elemsize,		/* In: Size (#bytes) per element */
                        const char *caller_file, int caller_line);	/* In */
                        '''

def __ckd_calloc_3d__(d1, d2, d3, elemsize, caller_file, caller_line):
    # char ***ref1, **ref2, *mem;
    # size_t i, j, offset;
    
    mem =  __ckd_calloc__(d1 * d2 * d3, elemsize, caller_file, caller_line)
    ref1 = __ckd_malloc__(d1 , caller_file, caller_line)
    ref2 = __ckd_malloc__(d1, caller_file, caller_line)
    
    # for (i = 0, offset = 0; i < d1; i++, offset += d2)
    i = 0
    offset = 0
    while(i < d1):
        ref1[i] = ref2 + offset
        i += 1
        offset += d2
    
    offset = 0
    for i in range(0 , d1):          # for (i = 0; i < d1; i++) {
        for j in range(0 , d2):  # for (j = 0; j < d2; j++) {
            ref1[i][j] = mem + offset
            offset += d3 * elemsize
    
    
    return ref1



# Macro for __ckd_calloc_3d__

def ckd_calloc_3d(d1,d2,d3,sz):
    return __ckd_calloc_3d__((d1),(d2),(d3),(sz))

'''/**
 * Free a 3-D array (ptr) previously allocated by ckd_calloc_3d
 */
void ckd_free_3d(void *ptr);
'''
def ckd_free_3d(inptr):
    ptr = inptr
    if (ptr and ptr[0]):
        ckd_free(ptr[0][0])
    if (ptr):
        ckd_free(ptr[0])
    ckd_free(ptr)



'''/**
 * Allocate a 34D array and return ptr to it.
 * The data area is allocated in one block so it can also be treated as a 1-D array.
 */
void ****__ckd_calloc_4d__(size_t d1, size_t d2, size_t d3, size_t d4, size_t elem_size, char *caller_file, int caller_line);
'''

def __ckd_calloc_4d__(d1, d2, d3, d4, elem_size, file, line):
    # void *store;
    # void **tmp1;
    # void ***tmp2;
    # void ****out;
    # size_t i, j;
    
    store = ckd_calloc(d1 * d2 * d3 * d4, elem_size)
    if (store == NULL):
        err.E_FATAL("ckd_calloc_4d failed for caller at %s(%d) at %s(%d)\n", file, line)
    
    
    tmp1 = ckd_calloc(d1 * d2 * d3, NULL)
    if (tmp1 == NULL):
        err.E_FATAL("ckd_calloc_4d failed for caller at %s(%d) at %s(%d)\n", file, line)
    
    
    tmp2 = ckd_calloc(d1 * d2, NULL)
    if (tmp2 == NULL):
        err.E_FATAL("ckd_calloc_4d failed for caller at %s(%d) at %s(%d)\n", file, line)
    
    
    out = ckd_calloc(d1, NULL)
    if (out == NULL):
        err.E_FATAL("ckd_calloc_4d failed for caller at %s(%d) at %s(%d)\n", file, line)
    
    j = 0
    for i in range(0 , d1*d2*d3):         # for (i = 0, j = 0; i < d1*d2*d3; i++, j += d4) 
        tmp1[i] = (store)[j*elem_size]
        j += d4
    
    j = 0
    for i in range(0 , d1*d2):         # for (i = 0, j = 0; i < d1*d2; i++, j += d3) {
        tmp2[i] = tmp1[j]
        j += d3
    
    j = 0
    for i in range(0 , d1):  # for (i = 0, j = 0; i < d1; i++, j += d2) {
        out[i] = tmp2[j]
    
    return out




# Macro for __ckd_calloc_4d__

def ckd_calloc_4d(d1, d2, d3, d4, s):
    return __ckd_calloc_4d__((d1), (d2), (d3), (d4), (s))

'''/**
 * Free a 4-D array (ptr) previously allocated by ckd_calloc_4d
 */
void ckd_free_4d(void *ptr);
'''

def ckd_free_4d(inptr):
    ptr = inptr
    if (ptr == NULL):
        return
    # free the underlying store */
    ckd_free(ptr[0][0][0])
    
    # free the access overhead */
    ckd_free(ptr[0][0])
    ckd_free(ptr[0])
    ckd_free(ptr)



'''/**
 * Overlay a 3-D array over a previously allocated storage area.
 **/
void * __ckd_alloc_3d_ptr(size_t d1, size_t d2, size_t d3, void *store, size_t elem_size, char *caller_file, int caller_line);

/* Layers a 3d array access structure over a preallocated storage area */   '''

def __ckd_alloc_3d_ptr(d1, d2, d3, store, elem_size, file, line):
    # void **tmp1;
    # void ***out;
    # size_t i, j;
    
    tmp1 = __ckd_calloc__(d1 * d2, NULL, file, line)
    
    out  = __ckd_calloc__(d1, NULL, file, line)
    
    j = 0
    for i in range(0 , d1*d2):        # for (i = 0, j = 0; i < d1*d2; i++, j += d3) {
        tmp1[i] = (store)[j*elem_size]
        j += d3
    
    j = 0
    for i in range(0 , d1):            # for (i = 0, j = 0; i < d1; i++, j += d2) {
        out[i] = tmp1[j]
        j += d2
    
    return out



#  Macro for __ckd_alloc_3d_ptr__
def ckd_alloc_3d_ptr(d1, d2, d3, bf, sz):
    return __ckd_alloc_3d_ptr((d1), (d2), (d3), (bf), (sz))

'''/**
 * Overlay a s-D array over a previously allocated storage area.
 **/
void *__ckd_alloc_2d_ptr(size_t d1, size_t d2, void *store, size_t elem_size, char *caller_file, int caller_line);
'''

def __ckd_alloc_2d_ptr(d1, d2, store, elem_size, file, line):
    # void **out;
    # size_t i, j;
    
    out = __ckd_calloc__(d1, NULL, file, line)
    
    j = 0
    for i in range(0 , d1):       # for (i = 0, j = 0; i < d1; i++, j += d2) {
        out[i] = (store)[j*elem_size]
        j += d2
    
    return out


#  vim: set ts=4 sw=4: */

# Macro for __ckd_alloc_2d_ptr__


def ckd_alloc_2d_ptr(d1, d2, bf, sz):    
    return __ckd_alloc_2d_ptr((d1), (d2), (bf), (sz))