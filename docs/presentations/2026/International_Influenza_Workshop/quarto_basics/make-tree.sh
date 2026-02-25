awk '
BEGIN{IGNORECASE=1}
# keep headers unchanged
/^>/ { print; next }
# sequence lines: replace anything not IUPAC with N
{
  gsub(/[^ACGTRYSWKMBDHVN-]/,"N")
  print toupper($0)
}
' gisaid_epiflu_sequence.fasta > cleaned.fa


docker run --rm   -u "$(id -u):$(id -g)" -v "$PWD":"$PWD" staphb/augur:latest \
    augur align \
    --sequences "$PWD"/cleaned.fa \
    --output "$PWD"/aligned.fa \
    --method mafft \
    --nthreads 12

docker run --rm -u "$(id -u):$(id -g)"  -v "$PWD":"$PWD" staphb/augur:latest \
    augur tree \
    --alignment "$PWD"/aligned.fa \
    --output "$PWD"/tree.nwk \
    --method iqtree \
    --tree-builder-args '-bb 1000 -bnni -czb' \
    --nthreads 12 \
    --override-default-args