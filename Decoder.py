from ps_decoder import ps_decoder_s as ps_decoder_t
from ps_decoder import cmd_ln_s as ps_astar_s
import ps_config
import ps_decoder
import logmath
import fsg
import ngram
import ps_alignment
NULL = 0
# <------------------------------------------------------------------------------------------------------------------->
# <------------------------------------------------------------------------------------------------------------------->
# <---------------------------------------- class Decoder: form main class ------------------------------------------->
# <------------------------------------------------------------------------------------------------------------------->
# <------------------------------------------------------------------------------------------------------------------->
class Decoder:
    """Main class for speech recognition and alignment in PocketSphinx.
    
    See :doc:`config_params` for a description of keyword arguments.
    
    Note that, as described in `Config`, `hmm`, `lm`, and `dict` are
    set to the default ones (some kind of US English models of unknown
    origin + CMUDict) if not defined.  You can prevent this by passing
    `None` for any of these parameters, e.g.::
    
        ps = Decoder(lm=None)  # Do not load a language model
    
    Decoder initialization **will fail** if more than one of `lm`,
    `jsgf`, `fsg`, `keyphrase`, `kws`, `allphone`, or `lmctl` are set
    in the configuration.  To make life easier, and because there is
    no possible case in which you would do this intentionally, if you
    initialize a `Decoder` or `Config` with any of these (and not
    `lm`), the default `lm` value will be removed.
    
    You can also pass a pre-defined `Config` object as the only
    argument to the constructor, e.g.::
    
        config = Config.parse_json(json)
        ps = Decoder(config)
    
    Args:
        config(Config): Optional configuration object.  You can also
                        use keyword arguments, the most important of
                        which are noted below.  See :doc:`config_params`
                        for more information.
        hmm(str): Path to directory containing acoustic model files.
        dict(str): Path to pronunciation dictionary.
        lm(str): Path to N-Gram language model.
        jsgf(str): Path to JSGF grammar file.
        fsg(str): Path to FSG grammar file (only one of ``lm``, ``jsgf``,
                or ``fsg`` should be specified).
        toprule(str): Name of top-level rule in JSGF file to use as entry point.
        samprate(int): Sampling rate for raw audio data.
        loglevel(str): Logging level, one of "INFO", "ERROR", "FATAL".
        logfn(str): File to write log messages to.
    Raises:
        ValueError: On invalid configuration or argument list.
        RuntimeError: On invalid configuration or other failure to
                    reinitialize decoder.
    """
    
    
    # cdef ps_decoder_t *_ps
    _ps = ps_decoder_t()
    
    #cdef Config _config
    _config = ps_config.Config()       # _config is the object of Config class
    # <---------------------------------------- Decoder Constructor ------------------------------------------->
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], ps_config.Config):
            self._config = args[0]
        else:
            # call the constructor __init__(self, *args, **kwargs) in Config class
            self._config = ps_config.Config(*args, **kwargs)
        if self._config is None:
            # raise ValueError, "Failed to parse argument list"
            print("Failed to parse argument list")
        self._ps = ps_decoder.ps_init(self._config.config)
        if (self._ps is None):
            # raise RuntimeError, "Failed to initialize PocketSphinx"
            print("Failed to initialize PocketSphinx")
    
    def __dealloc__(self):
        ps_decoder.ps_free(self._ps)
    
    # def reinit(self, Config config = None):
    def reinit(self, config = None):
        """Reinitialize the decoder.
        
        Args:
            config(Config): Optional new configuration to apply, otherwise
                            the existing configuration in the `config`
                            attribute will be reloaded.
        Raises:
            RuntimeError: On invalid configuration or other failure to reinitialize decoder.
        """
        cconfig = ps_config.ps_config_t() # cdef ps_config_t *cconfig
        if config is None:
            cconfig = NULL
        else:
            self._config = config
            cconfig = config.config
        if ps_decoder.ps_reinit(self._ps, cconfig) != 0:
            raise RuntimeError("Failed to reinitialize decoder configuration")
    
    # def reinit_feat(self, Config config=None):
    def reinit_feat(self, config=None):
        """Reinitialize only the feature extraction.
        
        Args:
            config(Config): Optional new configuration to apply, otherwise
                            the existing configuration in the `config`
                            attribute will be reloaded.
        Raises:
            RuntimeError: On invalid configuration or other failure to initialize feature extraction.
        """
        cconfig = ps_config.ps_config_t() # cdef ps_config_t *cconfig
        if config is None:
            cconfig = NULL
        else:
            self._config = config
            cconfig = config.config
        if (ps_decoder.ps_reinit_feat(self._ps, cconfig) < 0):
            raise RuntimeError("Failed to reinitialize feature extraction")
    
    def get_cmn(self, update=False):
        """Get current cepstral mean.
        
        Args:
            update(boolean): Update the mean based on current utterance.
        Returns:
            str: Cepstral mean as a comma-separated list of numbers.
        """
        cmn = ps_decoder.ps_get_cmn(self._ps, update) # cdef const char *cmn = ps_get_cmn(self._ps, update)
        return cmn.decode("utf-8")
    
    def set_cmn(self, cmn):
        """Get current cepstral mean.
        
        Args:
            cmn(str): Cepstral mean as a comma-separated list of numbers.
        """
        rv = ps_decoder.ps_set_cmn(self._ps, cmn.encode("utf-8")) # cdef int rv = ps_set_cmn(self._ps, cmn.encode("utf-8"))
        if rv != 0:
            raise ValueError("Invalid CMN string")
    
    def start_stream(self):
        """Reset noise statistics.
        
        This method can be called at the beginning of a new audio
        stream (but this is not necessary)."""
        rv = ps_decoder.ps_start_stream(self._ps)    # cdef int rv = ps_start_stream(self._ps)
        print("start_stream() is deprecated and unnecessary", DeprecationWarning)
        if rv < 0:
            raise RuntimeError("Failed to start audio stream")
    
    # <---------------------------------------- start_utt() ------------------------------------------->
    def start_utt(self):
        """Start processing raw audio input.
        
        This method must be called at the beginning of each separate
        "utterance" of raw audio input.
        
        Raises:
            RuntimeError: If processing fails to start (usually if it has already been started).
        """
        if (ps_decoder.ps_start_utt(self._ps) < 0):
            print("Failed to start utterance processing")
            # raise RuntimeError, "Failed to start utterance processing"
    # <-------------------------------------- get_in_speech() ------------------------------------------>
    def get_in_speech(self):
        """Return speech status.
        
        This method is retained for compatibility, but it will always
        return True as long as `ps_start_utt` has been previously
        called.
        """
        print("get_in_speech() is deprecated and does nothing useful", DeprecationWarning)
        return ps_decoder.ps_get_in_speech(self._ps)
    
    # <---------------------------------------- process_raw() ------------------------------------------->
    def process_raw(self, data, no_search=False, full_utt=False):
        """Process a block of raw audio.
        
        Args:
            data(bytes): Raw audio data, a block of 16-bit signed integer binary data.
            no_search(bool): If `True`, do not do any decoding on this data.
            full_utt(bool): If `True`, assume this is the entire utterance, for
                            purposes of acoustic normalization.
        Raises:
            RuntimeError: If processing fails.
        """
        cdata = data # cdef const unsigned char[:] cdata = data
        n_samples = len(cdata) // 2 # cdef Py_ssize_t n_samples = len(cdata) // 2
        ps_process_raws = ps_decoder.ps_process_raw(self._ps, cdata[0], n_samples, no_search, full_utt)
        if (ps_process_raws < 0):
            # raise RuntimeError, "Failed to process %d samples of audio data" % len / 2
            print(f'raise RuntimeError, "Failed to process {len / 2} samples of audio data')
    
    # <---------------------------------------- process_cep() ------------------------------------------->
    def process_cep(self, data, no_search=False, full_utt=False):
        """Process a block of MFCC data.
        
        Args:
            data(bytes): Raw MFCC data, a block of 32-bit floating point data.
            no_search(bool): If `True`, do not do any decoding on this data.
            full_utt(bool): If `True`, assume this is the entire utterance, for
                            purposes of acoustic normalization.
        Raises:
            RuntimeError: If processing fails.
        """
        cdata = data # cdef const unsigned char[:] cdata = data
        ncep = self._config["ceplen"] # cdef int ncep = self._config["ceplen"]
        nfr = len(cdata) // (ncep * len(float)) # cdef int nfr = len(cdata) // (ncep * sizeof(float))
        feats = NULL # cdef float **feats = <float **>ckd_alloc_2d_ptr(nfr, ncep, <void *>&cdata[0], sizeof(float))
        rv = ps_decoder.ps_process_cep(self._ps, feats, nfr, no_search, full_utt)
        # ckd_free(feats)
        if rv < 0:
            pass # raise RuntimeError, "Failed to process %d frames of MFCC data" % nfr
    
    
    # <---------------------------------------- end_utt() ------------------------------------------->
    def end_utt(self):
        """Finish processing raw audio input.
        
        This method must be called at the end of each separate
        "utterance" of raw audio input.  It takes care of flushing any
        internal buffers and finalizing recognition results.
        
        """
        ps_end_utts = ps_decoder.ps_end_utt(self._ps)
        if (ps_end_utts < 0):
            # raise RuntimeError, "Failed to stop utterance processing"
            print("raise RuntimeError ! Failed to stop utterance processing")
    
    
    # <---------------------------------------- hyp() ------------------------------------------->
    def hyp(self):
        """Get current recognition hypothesis.
        Returns:
            Hypothesis: Current recognition output.
        """
        hyp = ''                # cdef const char *hyp
        lmath = ps_decoder.logmath.logmath_t()     # cdef logmath_t *lmath
        score = 0               # cdef int score
        
        hyp = ps_decoder.ps_get_hyp(self._ps, score)
        if (hyp is None):   # NULL
            return None
        lmath = ps_config.ps_get_logmath(self._ps)
        prob = ps_decoder.ps_get_prob(self._ps)
        #return Hypothesis(hyp.decode('utf-8'), ps_decoder.logmath_exp(lmath, score), ps_decoder.logmath_exp(lmath, prob))
        return prob
    
    # <---------------------------------------- get_prob() ------------------------------------------->
    def get_prob(self):
        """Posterior probability of current recogntion hypothesis.
        
        Returns:
            float: Posterior probability of current hypothesis.  This
            will be 1.0 unless the `bestpath` configuration option is
            enabled.
        
        """
        # cdef logmath_t *lmath
        # cdef const char *uttid
        lmath = ps_config.ps_get_logmath(self._ps)
        return logmath.logmath_exp(lmath, ps_decoder.ps_get_prob(self._ps))
    
    # def add_word(self, str word, str phones, update=True):
    def add_word(self, word, phones, update=True):
        """Add a word to the pronunciation dictionary.
        
        Args:
            word(str): Text of word to be added.
            phones(str): Space-separated list of phones for this
                        word's pronunciation.  This will depend on
                        the underlying acoustic model but is probably
                        in ARPABET.
            update(bool): Update the recognizer immediately.  You can
                        set this to `False` if you are adding a lot
                        of words, to speed things up.
        Returns:
            int: Word ID of added word.
        Raises:
            RuntimeError: If adding word failed for some reason.
        """
        rv = ps_decoder.ps_add_word(self._ps, word.encode("utf-8"), phones.encode("utf-8"), update)
        if rv < 0:
            print("Failed to add word {word}")
    
    def lookup_word(self, word):
        """Look up a word in the dictionary and return phone transcription
        for it.
        
        Args:
            word(str): Text of word to search for.
        Returns:
            str: Space-separated list of phones, or None if not found.
        """
        
        cphones = ps_decoder.ps_lookup_word(self._ps, word.encode("utf-8"))
        if cphones == NULL:
            return None
        else:
            return cphones.decode("utf-8")
    
    def seg(self):
        """Get current word segmentation.
        
        Returns:
            Iterable[Segment]: Generator over word segmentations.
        """
        itor = ps_decoder.ps_seg_t   # cdef ps_seg_t *itor
        lmath = logmath.logmath_t()         # cdef logmath_t *lmath
        itor = ps_decoder.ps_seg_iter(self._ps)
        if itor == NULL:
            return
        lmath = ps_config.ps_get_logmath(self._ps)
        return ps_decoder.SegmentList.create(itor, lmath)
    
    
    def nbest(self):
        """Get N-Best hypotheses.
    
        Returns:
            Iterable[Hypothesis]: Generator over N-Best recognition results
        """
        itor = ps_decoder.ps_nbest_t # cdef ps_nbest_t *itor
        lmath = logmath.logmath_t()  # cdef logmath_t *lmath
        itor = ps_decoder.ps_nbest(self._ps)
        if itor == NULL:
            return
        lmath = ps_config.ps_get_logmath(self._ps)
        return ps_decoder.NBestList.create(itor, lmath)
    
    
    def read_fsg(self, filename):
        """Read a grammar from an FSG file.
        
        Args:
            filename(str): Path to FSG file.
        
        Returns:
            FsgModel: Newly loaded finite-state grammar.
        """
        # cdef float lw
        
        lw = ps_config.ps_config_float(self._config.config, "lw")
        return ps_config.FsgModel.readfile(filename, self.get_logmath(), lw)
    
    def read_jsgf(self, filename):
        """Read a grammar from a JSGF file.
        
        The top rule used is the one specified by the "toprule"
        configuration parameter.
        
        Args:
            filename(str): Path to JSGF file.
        Returns:
            FsgModel: Newly loaded finite-state grammar.
        """
        #cdef float lw
        
        lw = ps_config.ps_config_float(self._config.config, "lw")
        return ps_config.FsgModel.jsgf_read_file(filename, self.get_logmath(), lw)
    
    def create_fsg(self, name, start_state, final_state, transitions):
        """Create a finite-state grammar.
        
        This method allows the creation of a grammar directly from a
        list of transitions.  States and words will be created
        implicitly from the state numbers and word strings present in
        this list.  Make sure that the pronunciation dictionary
        contains the words, or you will not be able to recognize.
        Basic usage::
        
            fsg = decoder.create_fsg("mygrammar", start_state=0, final_state=3, transitions=[(0, 1, 0.75, "hello"), (0, 1, 0.25, "goodbye"),
            (1, 2, 0.75, "beautiful"), (1, 2, 0.25, "cruel"), (2, 3, 1.0, "world")])
        
        Args:
            name(str): Name to give this FSG (not very important).
            start_state(int): Index of starting state.
            final_state(int): Index of end state.
            transitions(list): List of transitions, each of which is a 3-
                                or 4-tuple of (from, to, probability[, word]).
                                If the word is not specified, this is an
                                epsilon (null) transition that will always be
                                followed.
        Returns:
            FsgModel: Newly created finite-state grammar.
        Raises:
            ValueError: On invalid input.
        """
        #cdef float lw
        #cdef int wid
        
        lw = ps_config.ps_config_float(self._config.config, "lw")
        lmath = self.get_logmath()
        n_state = max(ps_config.itertools.chain(*((t[0], t[1]) for t in transitions))) + 1
        fsg = ps_config.FsgModel(name, lmath, lw, n_state)
        fsg.set_start_state(start_state)
        fsg.set_final_state(final_state)
        for t in transitions:
            source, dest, prob = t[:3]
            if len(t) > 3:
                word = t[3]
                wid = fsg.word_add(word)
                if wid == -1:
                    raise ValueError(f"Failed to add word to FSG: {word}")
                fsg.trans_add(source, dest, lmath.log(prob), wid)
            else:
                fsg.null_trans_add(source, dest, lmath.log(prob))
        return fsg
    
    def parse_jsgf(self, jsgf_string, toprule=None):
        """Parse a JSGF grammar from bytes or string.
        
        Because PocketSphinx uses UTF-8 internally, it is more
        efficient to parse from bytes, as a string will get encoded
        and subsequently decoded.
        
        Args:
            jsgf_string(bytes|str): JSGF grammar as string or UTF-8
                                    encoded bytes.
            toprule(str): Name of starting rule in grammar (will default to first public rule).
        Returns:
            FsgModel: Newly loaded finite-state grammar.
        Raises:
            ValueError: On failure to parse or find `toprule`.
            RuntimeError: If JSGF has no public rules.
        """
        # cdef jsgf_t *jsgf
        # cdef jsgf_rule_t *rule
        # cdef logmath_t *lmath
        # cdef float lw

        if not isinstance(jsgf_string, bytes):
            jsgf_string = jsgf_string.encode("utf-8")
        jsgf = ps_config.jsgf_parse_string(jsgf_string, NULL)
        if jsgf == NULL:
            raise ValueError("Failed to parse JSGF")
        if toprule is not None:
            rule = ps_config.jsgf_get_rule(jsgf, toprule.encode('utf-8'))
            if rule == NULL:
                ps_config.jsgf_grammar_free(jsgf)
                raise ValueError(f"Failed to find top rule {toprule}")
        else:
            rule = ps_config.jsgf_get_public_rule(jsgf)
            if rule == NULL:
                ps_config.jsgf_grammar_free(jsgf)
                raise RuntimeError("No public rules found in JSGF")
        lw = ps_config.ps_config_float(self._config.config, "lw")
        lmath = ps_config.ps_get_logmath(self._ps)
        cfsg = ps_config.jsgf_build_fsg(jsgf, rule, lmath, lw)
        ps_config.jsgf_grammar_free(jsgf)
        return ps_config.FsgModel.create_from_ptr(ps_config.cfsg)
    
    def get_fsg(self, name = None):
        """Get the currently active FsgModel or the model for a
        specific search module.
        
        Args:
            name(str): Name of search module for this FSG.  If this is
                    None (the default), the currently active FSG will be
                    returned.
        Returns:
            FsgModel: FSG corresponding to `name`, or None if not found.
        """
        # cdef fsg_model_t *fsg 
        if name is None:
            fsg = ps_decoder.ps_get_fsg(self._ps, NULL)
        else:
            fsg = ps_decoder.ps_get_fsg(self._ps, name.encode("utf-8"))
        if fsg == NULL:
            return None
        else:
            return ps_config.create_from_ptr(fsg.fsg_model_retain(fsg))
    
    # def add_fsg(self, str name, FsgModel fsg):
    def add_fsg(self, name, fsg):
        """Create (but do not activate) a search module for a finite-state
        grammar.
        
        Args:
            name(str): Search module name to associate to this FSG.
            fsg(FsgModel): Previously loaded or constructed grammar.
        Raises:
            RuntimeError: If adding FSG failed for some reason.
        
        """
        if ps_decoder.ps_add_fsg(self._ps, name.encode("utf-8"), fsg.fsg) != 0:
            raise RuntimeError("Failed to set FSG in decoder")
    
    # def set_fsg(self, str name, FsgModel fsg):
    def set_fsg(self,name, fsg):
        # warnings.warn("set_fsg() is deprecated, use add_fsg() instead", DeprecationWarning)
        print("set_fsg() is deprecated, use add_fsg() instead", DeprecationWarning)
        self.add_fsg(name, fsg)
    
    def add_jsgf_file(self, name, filename):
        """Create (but do not activate) a search module from a JSGF file.
        
        Args:
            filename(str): Path to a JSGF file to load.
            name(str): Search module name to associate to this grammar.
        Raises:
            RuntimeError: If adding grammar failed for some reason.
        """
        if (ps_decoder.ps_add_jsgf_file(self._ps, name.encode("utf-8"), filename.encode()) != 0):
            raise RuntimeError("Failed to set JSGF from %s" % filename)
    
    def set_jsgf_file(self, name, filename):
        # warnings.warn("set_jsgf_file() is deprecated, use add_jsgf_file() instead", DeprecationWarning)
        print("set_jsgf_file() is deprecated, use add_jsgf_file() instead", DeprecationWarning)
        self.add_jsgf_file(name, filename)
    
    def add_jsgf_string(self, name, jsgf_string):
        """Create (but do not activate) a search module from JSGF
        as bytes or string.
        
        Args:
            jsgf_string(bytes|str): JSGF grammar as string or UTF-8 encoded
                                    bytes.
            name(str): Search module name to associate to this grammar.
        Raises:
            ValueError: If grammar failed to parse.
        """
        if not isinstance(jsgf_string, bytes):
            jsgf_string = jsgf_string.encode("utf-8")
        if (ps_decoder.ps_add_jsgf_string(self._ps, name.encode("utf-8"), jsgf_string) != 0):
            raise ValueError("Failed to parse JSGF in decoder")
    
    def set_jsgf_string(self, name, jsgf_string):
        # warnings.warn("set_jsgf_string() is deprecated, use add_jsgf_string() instead", DeprecationWarning)
        print("set_jsgf_string() is deprecated, use add_jsgf_string() instead", DeprecationWarning)
        self.add_jsgf_string(name, jsgf_string)
    
    def get_kws(self, name = None):
        """Get keyphrases as text from current or specified search module.
        
        Args:
            name(str): Search module name for keywords.  If this is
            None, the currently active keywords are returned if
            keyword search is active.
        Returns:
            str: List of keywords as lines (i.e. separated by '\\\\n'),
            or None if the specified search could not be found, or if
            `name` is None and keyword search is not currently active.
        """
        # cdef const char *kws
        if name is None:
            kws = ps_decoder.ps_get_kws(self._ps, NULL)
        else:
            kws = ps_decoder.ps_get_kws(self._ps, name.encode("utf-8"))
        if kws == NULL:
            return None
        else:
            return kws.decode("utf-8")
    
    def add_kws(self ,name, keyfile):
        """Create (but do not activate) keyphrase recognition search module
        from a file.
        
        Args:
            name(str): Search module name to associate to these keyphrases.
            keyfile(str): Path to file with list of keyphrases (one per line).
        Raises:
            RuntimeError: If adding keyphrases failed for some reason.
        """
        rv = ps_decoder.ps_add_kws(self._ps, name.encode("utf-8"), keyfile.encode())
        if rv < 0:
            return RuntimeError("Failed to set keyword search %s from %s" % (name, keyfile))
    
    def set_kws(self, name, keyfile):
        # warnings.warn("set_kws() is deprecated, use add_kws() instead", DeprecationWarning)
        print("set_kws() is deprecated, use add_kws() instead", DeprecationWarning)
        self.add_kws(name, keyfile)
    
    def add_keyphrase(self, name, keyphrase):
        """Create (but do not activate) search module from a single keyphrase.
        
        Args:
            name(str): Search module name to associate to this keyphrase.
            keyphrase(str): Keyphrase to add.
        Raises:
            RuntimeError: If adding keyphrase failed for some reason.
        """
        rv = ps_decoder.ps_add_keyphrase(self._ps, name.encode("utf-8"), keyphrase.encode("utf-8"))
        if rv < 0:
            return RuntimeError("Failed to set keyword search %s from phrase %s"
                                % (name, keyphrase))
    
    def set_keyphrase(self, name, keyphrase):
        # warnings.warn("set_keyphrase() is deprecated, use add_keyphrase() instead", DeprecationWarning)
        print("set_keyphrase() is deprecated, use add_keyphrase() instead", DeprecationWarning)
        self.add_keyphrase(name, keyphrase)
    
    def add_allphone_file(self, name, lmfile = None):
        """Create (but do not activate) a phoneme recognition search module.
        
        Args:
            name(str): Search module name to associate to allphone search.
            lmfile(str): Path to phoneme N-Gram file, or None to use
                        uniform probability (default is None)
        Raises:
            RuntimeError: If allphone search init failed for some reason.
        """
        # cdef int rv
        if lmfile is None:
            rv = ps_decoder.ps_add_allphone_file(self._ps, name.encode("utf-8"), NULL)
        else:
            rv = ps_decoder.ps_add_allphone_file(self._ps, name.encode("utf-8"), lmfile.encode())
        if rv < 0:
            return RuntimeError("Failed to set allphone search %s from %s"% (name, lmfile))
    
    def set_allphone_file(self, name, keyfile):
        # warnings.warn("set_allphone_file() is deprecated, use add_allphone_file() instead", DeprecationWarning)
        print("set_allphone_file() is deprecated, use add_allphone_file() instead", DeprecationWarning)
        self.add_allphone_file(name, keyfile)
    
    def get_lattice(self):
        """Get word lattice from current recognition result.
        
        Returns:
            Lattice: Word lattice from current result.
        """
        lattice = ps_decoder.ps_get_lattice(self._ps)
        if lattice == NULL:
            return None
        return ps_config.create_from_ptr(ps_decoder.ps_lattice_retain(lattice))
    
    # @property
    def config(self):
        """Read-only property containing configuration object."""
        return self._config
    
    def get_config(self):
        """Get current configuration.
        
        DEPRECATED: This does the same thing as simply accessing
        `config` and is here for historical reasons.
        
        Returns:
            Config: Current configuration.
        
        """
        return self._config
    
    # These two do not belong here but they're here for compatibility
    # @staticmethod
    def default_config():
        """Get the default configuration.
        
        DEPRECATED: This does the same thing as simply creating a
        `Config` and is here for historical reasons.
        
        Returns:
            Config: Default configuration.
        """
        # warnings.warn("default_config() is deprecated, just call Config() constructor", DeprecationWarning)
        print("default_config() is deprecated, just call Config() constructor", DeprecationWarning)
        return ps_config.Config()
    
    # @staticmethod
    def file_config(path):  # sourcery skip: instance-method-first-arg-name
        """Parse configuration from a file.
        
        DEPRECATED: This simply calls `Config.parse_file` and is here
        for historical reasons.
        
        Args:
            path(str): Path to arguments file.
        Returns:
            Config: Configuration parsed from `path`.
        """
        # warnings.warn("file_config() is deprecated, use JSON configuration please", DeprecationWarning)
        print("file_config() is deprecated, use JSON configuration please", DeprecationWarning)
        return ps_config.Config.parse_file(path)
    
    def load_dict(self, dict_path, fdict_path = None, _format = None):
        """Load dictionary (and possibly noise dictionary) from a file.
        
        Note that the `format` argument does nothing, never has done
        anything, and never will.  It's only here for historical
        reasons.
        
        Args:
            dict_path(str): Path to pronunciation dictionary file.
            fdict_path(str): Path to noise dictionary file, or None to keep
                            existing one (default is None)
            _format(str): Useless argument that does nothing.
        Raises:
            RuntimeError: If dictionary loading failed for some reason.
        """
        # cdef int rv
        # THIS IS VERY ANNOYING, CYTHON
        cformat = NULL # cdef const char *cformat = NULL
        cdict = NULL   # cdef const char *cdict = NULL
        cfdict = NULL  # cdef const char *cfdict = NULL
        if _format is not None:
            spam = _format.encode("utf-8")
            cformat = spam
        if dict_path is not None:
            eggs = dict_path.encode()
            cdict = eggs
        if fdict_path is not None:
            bacon = fdict_path.encode()
            cfdict = bacon
        rv = ps_decoder.ps_load_dict(self._ps, cdict, cfdict, cformat)
        if rv < 0:
            raise RuntimeError("Failed to load dictionary from %s and %s" % (dict_path, fdict_path))
    
    def save_dict(self, dict_path, _format = None):
        """Save dictionary to a file.
        
        Note that the `format` argument does nothing, never has done
        anything, and never will.  It's only here for historical
        reasons.
        
        Args:
            dict_path(str): Path to save pronunciation dictionary in.
            _format(str): Useless argument that does nothing.
        Raises:
            RuntimeError: If dictionary saving failed for some reason.
        """
        # cdef int rv
        cformat = NULL  # cdef const char *cformat = NULL
        cdict = NULL    # cdef const char *cdict = NULL
        if _format is not None:
            spam = _format.encode("utf-8")
            cformat = spam
        if dict_path is not None:
            eggs = dict_path.encode()
            cdict = eggs
        rv = ps_decoder.ps_save_dict(self._ps, cdict, cformat)
        if rv < 0:
            raise RuntimeError("Failed to save dictionary to %s" % dict_path)
    
    def get_lm(self, name = None):
        """Get the current N-Gram language model or the one associated with a
        search module.
        
        Args:
            name(str): Name of search module for this language model.  If this
                        is None (default) the current LM will be returned.
        Returns:
            NGramModel: Model corresponding to `name`, or None if not found.
        
        """
        lm = ngram.ngram_model_t() # cdef ngram_model_t *lm
        if name is None:
            lm = ps_decoder.ps_get_lm(self._ps, NULL)
        else:
            lm = ps_decoder.ps_get_lm(self._ps, name.encode("utf-8"))
        if lm == NULL:
            return None
        return ps_config.create_from_ptr(ngram.ngram_model_retain(lm))
    
    def add_lm(self, name, lm):  # (self, str name, NGramModel lm):
        """Create (but do not activate) a search module for an N-Gram language
        model.
        
        Args:
            name(str): Search module name to associate to this LM.
            lm(NGramModel): Previously loaded language model.
        Raises:
            RuntimeError: If adding LM failed for some reason.
        """
        rv = ps_decoder.ps_add_lm(self._ps, name.encode("utf-8"), lm.lm)
        if rv < 0:
            raise RuntimeError("Failed to set language model %s" % name)
    
    def set_lm(self, name, lm):
        # warnings.warn("set_lm() is deprecated, use add_lm() instead", DeprecationWarning)
        print("set_lm() is deprecated, use add_lm() instead", DeprecationWarning)
        self.add_lm(name, lm)
    
    def add_lm_file(self, name, path):
        """Load (but do not activate a language model from a file into the
        decoder.
        
        Args:
            name(str): Search module name to associate to this LM.
            path(str): Path to N-Gram language model file.
        Raises:
            RuntimeError: If adding LM failed for some reason.
        """
        rv = ps_decoder.ps_add_lm_file(self._ps, name.encode("utf-8"), path.encode())
        if rv < 0:
            raise RuntimeError("Failed to set language model %s from %s" % (name, path))
    
    def set_lm_file(self, name, path):
        # warnings.warn("set_lm_file() is deprecated, use add_lm_file() instead",  DeprecationWarning)
        print("set_lm_file() is deprecated, use add_lm_file() instead",  DeprecationWarning)
        self.add_lm_file(name, path)
    
    # @property
    def logmath(self):
        """Read-only property containing LogMath object for this decoder."""
        return self.get_logmath()
    
    def get_logmath(self):
        """Get the LogMath object for this decoder.
        
        DEPRECATED: This does the same thing as simply accessing
        `logmath` and is here for historical reasons.
        
        Returns:
            LogMath: Current log-math computation object.
        """
        lmath = (self._ps)  # cdef logmath_t *lmath
        return ps_config.create_from_ptr(logmath.logmath_retain(lmath))
    
    def activate_search(self, search_name = None):
        """Activate a search module
        
        This activates a "search module" that was created with the
        methods `add_fsg`, `add_lm`, `add_lm_file`,
        `add_allphone_file`, `add_keyphrase`, or `add_kws`.
        
        This API is still bad, but at least the method names make
        sense now.
        
        Args:
            search_name(str): Name of search module to activate.  If
            None (or not given), then the default search module, the
            one created with the Decoder, for instance, will be
            (re-)activated.
        
        Raises:
            KeyError: If `search_name` doesn't actually exist.
        
        """
        # cdef int rv
        if search_name is None:
            rv = ps_decoder.ps_activate_search(self._ps, NULL)
        else:
            rv = ps_decoder.ps_activate_search(self._ps, search_name.encode("utf-8"))
        if rv < 0:
            raise KeyError("Unable to set search %s" % search_name)
    
    def set_search(self, search_name):
        # warnings.warn("set_search() is deprecated, use activate_search() instead", DeprecationWarning)
        print("set_search() is deprecated, use activate_search() instead", DeprecationWarning)
        self.activate_search(search_name)
    
    def remove_search(self, search_name):
        """Remove a search (LM, grammar, etc) freeing resources.
        
        Args:
            search_name(str): Name of search module to remove.
        Raises:
            KeyError: If `search_name` doesn't actually exist.
        """
        rv = ps_decoder.ps_remove_search(self._ps, search_name.encode("utf-8"))
        if rv < 0:
            raise KeyError("Unable to unset search %s" % search_name)
    
    def unset_search(self, search_name):
        # warnings.warn("unset_search() is deprecated, use remove_search() instead", DeprecationWarning)
        print("unset_search() is deprecated, use remove_search() instead", DeprecationWarning)
        self.remove_search(search_name)
    
    def current_search(self):
        """Get the name of the current search (LM, grammar, etc).
        
        Returns:
            str: Name of currently active search module.
        """
        return ps_decoder.ps_current_search(self._ps).decode("utf-8")
    
    def get_search(self):
        # warnings.warn("get_search() is deprecated, use current_search() instead", DeprecationWarning)
        print("get_search() is deprecated, use current_search() instead", DeprecationWarning)
        return self.current_search()
    
    def set_align_text(self, text):
        """Set a word sequence for alignment *and* enable alignment mode.
        
        Unlike the `add_*` methods and the deprecated, badly-named
        `set_*` methods, this really does immediately enable the
        resulting search module.  This is because alignment is
        typically a one-shot deal, i.e. you are not likely to create a
        list of different alignments and keep them around.  If you
        really want to do that, perhaps you should use FSG search
        instead.  Or let me know and perhaps I'll add an
        `add_align_text` method.
        
        You must do any text normalization yourself.  For word-level
        alignment, once you call this, simply decode and get the
        segmentation in the usual manner.  For phone-level alignment,
        see `set_alignment` and `get_alignment`.
        
        Args:
            text(str): Sentence to align, as whitespace-separated
                        words.  All words must be present in the
                        dictionary.
        Raises:
            RuntimeError: If text is invalid somehow.
        """
        rv = ps_decoder.ps_set_align_text(self._ps, text.encode("utf-8"))
        if rv < 0:
            raise RuntimeError("Failed to set up alignment of %s" % (text))
    
    # def set_alignment(self, Alignment alignment = None):
    def set_alignment(self, alignment = None):
        """Set up *and* activate sub-word alignment mode.
        
        For efficiency reasons, decoding and word-level alignment (as
        done by `set_align_text`) do not track alignments at the
        sub-word level.  This is fine for a lot of use cases, but
        obviously not all of them.  If you want to obtain phone or
        state level alignments, you must run a second pass of
        alignment, which is what this function sets you up to do.  The
        sequence is something like this::
        
            decoder.set_align_text("hello world")
            decoder.start_utt()
            decoder.process_raw(data, full_utt=True)
            decoder.end_utt()
            decoder.set_alignment()
            decoder.start_utt()
            decoder.process_raw(data, full_utt=True)
            decoder.end_utt()
            for word in decoder.get_alignment():
                for phone in word:
                    for state in phone:
                        print(word, phone, state)
        
        That's a lot of code, so it may get simplified, either here or
        in a derived class, before release.
        
        Note that if you are using this with N-Gram or FSG decoding,
        you can restore the default search module afterwards by
        calling activate_search() with no argument.
        
        Args:
            alignment(Alignment): Pre-constructed `Alignment` object.
                    Currently you can't actually do anything with this.
        Raises:
            RuntimeError: If current hypothesis cannot be aligned (such
                            as when using keyphrase or allphone search).
        
        """
        # cdef int rv
        if alignment is not None:
            rv = ps_decoder.ps_set_alignment(self._ps, alignment._al)
        else:
            rv = ps_decoder.ps_set_alignment(self._ps, NULL)
        if rv < 0:
            raise RuntimeError("Failed to set up sub-word alignment")
    
    def get_alignment(self):
        """Get the current sub-word alignment, if any.
        
        This will return something if `ps_set_alignment` has been
        called, but it will not contain an actual *alignment*
        (i.e. phone and state durations) unless a second pass of
        decoding has been run.
        
        If the decoder is not in sub-word alignment mode then it will
        return None.
        
        Returns:
            Alignment - if an alignment exists.
        """
        al = ps_decoder.ps_get_alignment(self._ps)  # cdef ps_alignment_t *al = ps_get_alignment(self._ps)
        if al == NULL:
            return None
        return ps_config.create_from_ptr(ps_alignment.ps_alignment_retain(al))
    
    def n_frames(self):
        """Get the number of frames processed up to this point.
        
        Returns:
            int: Like it says.
        """
        return ps_decoder.ps_get_n_frames(self._ps)
