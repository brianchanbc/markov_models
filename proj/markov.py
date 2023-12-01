from hashtable import Hashtable
from collections import defaultdict
import math

# parameters for Hashtable
HASH_CELLS = 57
DEFAULT_VALUE = 0
TOO_FULL = 0.5
GROWTH_RATIO = 2

class Markov:
    def __init__(self, k, text, use_hashtable):
        """
        Construct a new k-order markov model using the text 'text'.
        
        args:
            k: order of the model
            text: text to train the model
            use_hashtable: boolean to indicate whether to use hashtable or dict
        """
        self.k = k
        self.text = text
        self.use_hashtable = use_hashtable
        if use_hashtable:
            self.model_table = Hashtable(HASH_CELLS, DEFAULT_VALUE, TOO_FULL, GROWTH_RATIO)
        else:
            self.model_table = defaultdict(lambda: DEFAULT_VALUE)
        self.uniq_chars = set()
        # train the model
        self._train(k, text, self.model_table, self.uniq_chars)

    @staticmethod
    def wrap_str(str, start_index, k):
        """
        Circular wrap on string to continue to read the string
        from the beginning when it is reached the end.
        
        args:
            str: string to wrap
            start_index: starting index
            k: order of the model
        
        returns:
            wrapped string
        """
        if not str:
            return None
        end = start_index + k
        if end <= len(str):
            return str[start_index:end]
        # wrap around needed
        end_wrap = end - len(str)
        return str[start_index:] + str[:end_wrap]
    
    def _train(self, k, text, model, uniq_chars):    
        """
        Initialize the trained model
        
        Args:
            k: order of the model
            text: text to train the model
            model: model to be trained
            uniq_chars: unique characters in the text
        """           
        for i, char in enumerate(text):
            # get the k+1-order strings
            k1_str = Markov.wrap_str(text, i, k+1)
            # frequency of k_str and k1_str add 1
            model[k1_str[:-1]] += 1
            model[k1_str] += 1
            # add unique character
            uniq_chars.add(char)
    
    def log_probability(self, str):
        """
        Get the log probability of string "s", given the statistics of
        character sequences modeled by this particular Markov model
        This probability is *not* normalized by the length of the string.
        
        args:
            s: string to get log probability
            
        returns:
            log probability of string "s"
        """ 
        num_uniq_chars = len(self.uniq_chars)
        likelihood = 0
        n = len(str)
        for i in range(n):
            # get the k+1-order strings
            k1_str = Markov.wrap_str(str, i, self.k+1)
            # calculate the log probability
            freq_str_k = self.model_table[k1_str[:-1]]
            freq_str_k1 = self.model_table[k1_str]
            prob = math.log((freq_str_k1 + 1) / (freq_str_k + num_uniq_chars))
            # add to the likelihood
            likelihood += prob
        return likelihood

def identify_speaker(speech1, speech2, speech3, k, use_hashtable):
    """
    Given sample text from two speakers (1 and 2), and text from an
    unidentified speaker (3), return a tuple with the *normalized* log probabilities
    of each of the speakers uttering that text under a "order" order
    character-based Markov model, and a conclusion of which speaker
    uttered the unidentified text based on the two probabilities.
    """
    # initialize models for speech1 and speech2
    model_1 = Markov(k, speech1, use_hashtable)
    model_2 = Markov(k, speech2, use_hashtable)
    # calculate the log probability of speech3 using model_1 and model_2
    model_1_prob = model_1.log_probability(speech3) / len(speech3)
    model_2_prob = model_2.log_probability(speech3) / len(speech3)
    # return the normalized log probabilities and the conclusion
    if model_1_prob > model_2_prob:
        return (model_1_prob, model_2_prob, "A")
    return (model_1_prob, model_2_prob, "B")