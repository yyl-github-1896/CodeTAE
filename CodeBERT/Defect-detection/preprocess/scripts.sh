CUDA_VISIBLE_DEVICES=2 python get_substitutes.py \
    --store_path ./dataset/test_subs_0_400.jsonl \
    --base_model=microsoft/codebert-base-mlm \
    --eval_data_file=./dataset/test.jsonl \
    --block_size 512


# CUDA_VISIBLE_DEVICES=2 python get_substitutes_gan.py \
#     --store_path ./dataset/test_subs_gan_0_400.jsonl \
#     --base_model=microsoft/codebert-base-mlm \
#     --eval_data_file=./dataset/test.jsonl \
#     --block_size 512