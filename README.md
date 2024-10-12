



# HW4_package

## Description

This program filters FASTQ sequences based on GC content, sequence length, and quality score using the *phred33* scale. After filtering, the program can apply DNA/RNA sequence processing tools (such as transcription, reverse, complement, or reverse complement) to the filtered sequences.

Key Features:

* `filter_fastq`: Filters FASTQ sequences based on user-defined criteria such as GC content, sequence length, and quality thresholds.
* `run_dna_rna_tools`: Applies DNA/RNA sequence operations like transcription, reverse, complement, or reverse complement.

## Installation

To use this package, follow these steps:

Download the HW4_package_main.py script and the source folder with supplementary modules: `suppl_filter_fastq.py`, `suppl_run_dna_rna_tools.py`, and `bio_files_processor.py`. Ensure all modules are located within the `source/` directory.

To clone the repository using Git:
```bash
git clone git@github.com:vsubrakova/HW4_package.git
```
After downloading the script, you can import the functions into your own script:
```python
from HW4_package_main import filter_fastq, run_dna_rna_tools
```
## Usage

### ```filter_fastq(seqs, gc_bounds, length_bounds, quality_threshold)```
The function reads .fastq file and filters sequences based on GC content, sequence length, and quality score thresholds.

**Arguments**:
* `input_fastq` (str): Path to the FASTQ file. Can be absolute or relative. If a relative path is used, place the `.fastq` file in the `input_data` folder and provide only the file name, as shown in the example.
* `gc_bounds` (int or tuple, optional): The GC content range for filtering. If an integer is provided, it is treated as an upper bound with 0 as the lower bound. *Default is (0, 100)*.
* `length_bounds` (int or tuple, optional): The sequence length range for filtering. If an integer is provided, it is treated as an upper bound with 0 as the lower bound. *Default is (0, 2\*\*32)*.
* `quality_threshold` (float, optional): The minimum average quality threshold (phred33 scale). *Default is 0*.
* `output_fastq` (str, optional): If provided, the filtered sequences will be written to a  file in the `filtered/ ` directory with this name. If not, function will store filtered sequence as a dictionary.

**Returns**:
- A new dictionary containing only sequences that meet the filtering criteria. 

**Usage Scenarios**
* Writing filtered sequences to an output file

If the `output_fastq` argument is provided (e.g., a file name like "banana.py"), the function will:
   * Filter the sequences based on the specified criteria.
   * Write the filtered sequences to the file specified by the output_fastq parameter.
No dictionary is returned by the function in this case, the results are saved directly to the file.

Example:
```python
filtered_fastq = filter_fastq(
    input_fastq="example_fastq.fastq",
    gc_bounds=(40, 60),
    length_bounds=(50, 100),
    quality_threshold=30,
    output_fastq="banana.py", # Returns output file with filtered sequences
)
```
```python
# output example
filtered_fastq = {
    '@SRX079804:1:SRR292678:1:1101:24563:24563 1:N:0:1 BH:failed': ('ATTAGCGAGGAGGAGTGCTGAGAAGATGTCGCCTACGCCGTTGAAATTCCCTTCAATCAGGGGGTACTGGAGGATACGAGTTTGTGTG','BFFFFFFFB@B@A<@D>DDACDDDEBEDEFFFBFFFEFFDFFF=CC@DDFD8FFFFFFF8/+.2,@7<<:?B/:<><-><@.A*C>D')}
```

* Returning filtered sequences as a dictionary

If the output_fastq argument is not provided (or set to None), the function will:
    * Filter the sequences based on the specified criteria.
    * Return the filtered sequences as a dictionary without writing to any output file.

```python
seqs = filter_fastq(
    input_fastq="example_fastq.fastq",
    gc_bounds=(40, 60),
    length_bounds=(50, 100),
    quality_threshold=30,
    output_fastq=None  # No output file, returns dictionary
)
print(seqs) 
```


### ```run_dna_rna_tools(*args, results=None)```
The function performs a specified operation (e.g., transcription or reverse complement) on one or more DNA/RNA sequences.

**Arguments**:
* `*args` (str): Variable-length argument list where the last argument is the name of the operation, and the preceding arguments are DNA/RNA sequences.
* `results` (list, optional): A list to store the results of the operations. Default is `None`).

**Returns**:
* A string (for a single sequence) or a list (for multiple sequences) containing the results of the operation.

**Available Operations**:
- `transcribe`:  Converts a DNA sequence into RNA.
- `reverse`: Reverses the sequence.
- `complement`: Returns the complementary DNA sequence.
- `reverse_complement`: Returns the reverse complement of the DNA sequence.

**Example**:
```python
result = run_dna_rna_tools("AGCTAGC", "CGATCGA", "transcribe")
print(result)  # Output: ['AGCUAGC', 'CGAUCGA']
```

