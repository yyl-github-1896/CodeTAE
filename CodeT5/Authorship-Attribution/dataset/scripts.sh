CUDA_VISIBLE_DEVICES=4 python get_substitutes.py \
    --store_path ./data_folder/processed_gcjpy/valid_subs.jsonl \
    --base_model=microsoft/codebert-base-mlm \
    --eval_data_file=./data_folder/processed_gcjpy/valid.txt \
    --block_size 512


# CUDA_VISIBLE_DEVICES=4 python get_substitutes_gan.py \
#     --store_path ./data_folder/processed_gcjpy/valid_subs_gan.jsonl \
#     --base_model=microsoft/codebert-base-mlm \
#     --eval_data_file=./data_folder/processed_gcjpy/valid.txt \
#     --block_size 512