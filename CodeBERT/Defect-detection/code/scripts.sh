#train
CUDA_VISIBLE_DEVICES=0 python run.py \
    --output_dir=./saved_models \
    --model_type=roberta \
    --tokenizer_name=microsoft/codebert-base \
    --model_name_or_path=microsoft/codebert-base \
    --do_train \
    --train_data_file=../preprocess/dataset/train.jsonl \
    --eval_data_file=../preprocess/dataset/test_subs_0_400.jsonl \
    --test_data_file=../preprocess/dataset/test.jsonl \
    --epoch 5 \
    --block_size 512 \
    --train_batch_size 32 \
    --eval_batch_size 64 \
    --learning_rate 2e-5 \
    --max_grad_norm 1.0 \
    --evaluate_during_training \
    --seed 123456


#eval_asr
# CUDA_VISIBLE_DEVICES=3 python run.py \
#     --output_dir=./saved_models \
#     --model_type=roberta \
#     --tokenizer_name=microsoft/codebert-base \
#     --model_name_or_path=microsoft/codebert-base \
#     --do_asr \
#     --train_data_file=../preprocess/dataset/train.jsonl \
#     --eval_data_file=../preprocess/dataset/valid.jsonl \
#     --test_data_file=../preprocess/dataset/test_subs_0_400.jsonl \
#     --adv_data_file=./advs_transfer/adv_codebert_ablation_ensemble_untargeted.txt \
#     --epoch 5 \
#     --block_size 512 \
#     --train_batch_size 32 \
#     --eval_batch_size 64 \
#     --learning_rate 2e-5 \
#     --max_grad_norm 1.0 \
#     --evaluate_during_training \
#     --seed 123456


#attack
# CUDA_VISIBLE_DEVICES=2 python attack_ablation_ensemble.py \
#     --output_dir=./saved_models \
#     --model_type=roberta \
#     --tokenizer_name=microsoft/codebert-base-mlm \
#     --model_name_or_path=microsoft/codebert-base-mlm \
#     --csv_store_path ./attack_genetic.csv \
#     --base_model=microsoft/codebert-base-mlm \
#     --use_ga \
#     --train_data_file=../preprocess/dataset/train_subs.jsonl \
#     --eval_data_file=../preprocess/dataset/test_subs_0_400.jsonl \
#     --eval_data_file_2=../preprocess/dataset/test_subs_gan_0_400.jsonl \
#     --test_data_file=../preprocess/dataset/test_subs.jsonl \
#     --block_size 512 \
#     --eval_batch_size 64 \
#     --num_of_changes 2 \
#     --seed 123456


#attack_mhm
# CUDA_VISIBLE_DEVICES=3 python attack_mhm.py \
#     --output_dir=./saved_models \
#     --model_type=roberta \
#     --tokenizer_name=microsoft/codebert-base \
#     --model_name_or_path=microsoft/codebert-base \
#     --csv_store_path ./attack_mhm_ls.csv \
#     --base_model=microsoft/codebert-base-mlm \
#     --train_data_file=../preprocess/dataset/train_subs.jsonl \
#     --eval_data_file=../preprocess/dataset/test_subs_baseline_0_400.jsonl \
#     --test_data_file=../preprocess/dataset/test_subs.jsonl \
#     --block_size 512 \
#     --eval_batch_size 64 \
#     --seed 123456


#attack_alert
# CUDA_VISIBLE_DEVICES=0 python attack_alert.py \
#     --output_dir=./saved_models \
#     --model_type=roberta \
#     --tokenizer_name=microsoft/codebert-base-mlm \
#     --model_name_or_path=microsoft/codebert-base-mlm \
#     --csv_store_path ./attack_genetic.csv \
#     --base_model=microsoft/codebert-base-mlm \
#     --use_ga \
#     --train_data_file=../preprocess/dataset/train_subs.jsonl \
#     --eval_data_file=../preprocess/dataset/test_subs_baseline_0_400.jsonl \
#     --test_data_file=../preprocess/dataset/test_subs.jsonl \
#     --block_size 512 \
#     --eval_batch_size 64 \
#     --seed 123456