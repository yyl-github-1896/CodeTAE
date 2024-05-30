CUDA_VISIBLE_DEVICES=5 python get_substitutes.py \
    --store_path ./data_folder/processed_gcjpy/valid_subs.jsonl \
    --base_model=microsoft/graphcodebert-base \
    --eval_data_file=./data_folder/processed_gcjpy/valid.txt \
    --block_size 512


# CUDA_VISIBLE_DEVICES=5 python get_substitutes_gan.py \
#     --store_path ./data_folder/processed_gcjpy/valid_subs_gan.jsonl \
#     --base_model=microsoft/graphcodebert-base \
#     --eval_data_file=./data_folder/processed_gcjpy/valid.txt \
#     --block_size 512


# CUDA_VISIBLE_DEVICES=4 python get_substitutes_nsga.py \
#     --store_path ./data_folder/processed_gcjpy/valid_subs_nsga.jsonl \
#     --base_model=microsoft/graphcodebert-base \
#     --eval_data_file=./data_folder/processed_gcjpy/valid.txt \
#     --block_size 512