# CUDA_VISIBLE_DEVICES=1 python get_substitutes.py \
#     --store_path ./test_subs_0_500_.jsonl \
#     --base_model=microsoft/codebert-base-mlm \
#     --eval_data_file=./test_sampled.txt \
#     --block_size 512 \
#     --index 0 500


CUDA_VISIBLE_DEVICES=0 python get_substitutes_gan.py \
    --store_path ./test_subs_gan_0_500.jsonl \
    --base_model=microsoft/codebert-base-mlm \
    --eval_data_file=./test_sampled.txt \
    --block_size 512 \
    --index 0 500