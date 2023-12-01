import sys
from pathlib import Path
from markov import identify_speaker

def read_file(filename):
    """helper function to read file

    Args:
        filename: name of the file to read

    Returns:
        content of the file
    """
    path = Path(__file__).parent / filename
    with path.open() as f:
        return f.read()

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print(
            f"Usage: python3 {sys.argv[0]} <filenameA> <filenameB> <filenameC> <k> <hashtable-or-dict>"
        )
        sys.exit(1)

    # extract parameters from command line & convert types
    filenameA, filenameB, filenameC, k, hashtable_or_dict = sys.argv[1:]
    k = int(k)
    if hashtable_or_dict not in ("hashtable", "dict"):
        print("Final parameter must either be 'hashtable' or 'dict'")
        sys.exit(1)

    # TODO: add code here to open files & read text        
    speech1 = read_file(filenameA)
    speech2 = read_file(filenameB)
    speech3 = read_file(filenameC)
    
    # TODO: add code to call identify_speaker & print results
    speaker1_pr, speaker2_pr, speaker = \
        identify_speaker(speech1, speech2, speech3, k, hashtable_or_dict)
        
    print(f"Speaker A: {speaker1_pr}")
    print(f"Speaker B: {speaker2_pr}\n")
    print(f"Conclusion: Speaker {speaker} is most likely")
    
    # Output should resemble (values will differ based on inputs):

    # Speaker A: -2.1670591295191572
    # Speaker B: -2.2363636778055525

    # Conclusion: Speaker A is most likely
