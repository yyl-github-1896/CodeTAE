#train
python run.py \
    --output_dir=./saved_models \
    --model_type=roberta \
    --config_name=microsoft/codebert-base \
    --model_name_or_path=microsoft/codebert-base \
    --tokenizer_name=roberta-base \
    --do_train \
    --train_data_file=../dataset/train_sampled.txt \
    --eval_data_file=../dataset/valid_sampled.txt \
    --test_data_file=../dataset/test_sampled.txt \
    --epoch 2 \
    --block_size 512 \
    --train_batch_size 16 \
    --eval_batch_size 32 \
    --learning_rate 5e-5 \
    --max_grad_norm 1.0 \
    --evaluate_during_training \
    --seed 123456


#eval_asr
# CUDA_VISIBLE_DEVICES=0 python run.py \
#     --output_dir=./saved_models \
#     --model_type=roberta \
#     --config_name=microsoft/codebert-base \
#     --model_name_or_path=microsoft/codebert-base \
#     --tokenizer_name=roberta-base \
#     --do_asr \
#     --train_data_file=../dataset/train_sampled.txt \
#     --eval_data_file=../dataset/valid_sampled.txt \
#     --test_data_file=../dataset/test_sampled_0_500.txt \
#     --adv_data_file=./advs_transfer/adv_codebert_ablation_ensemble.txt \
#     --eval_batch_size 16 \
#     --seed 123456


#attack
# CUDA_VISIBLE_DEVICES=0 python attack_ablation_ensemble.py \
#     --output_dir=./saved_models \
#     --model_type=roberta \
#     --config_name=microsoft/codebert-base \
#     --csv_store_path ./attack_base_result_GA.csv \
#     --model_name_or_path=microsoft/codebert-base \
#     --tokenizer_name=roberta-base \
#     --use_ga \
#     --base_model=microsoft/codebert-base-mlm \
#     --train_data_file=../dataset/train_sampled.txt \
#     --eval_data_file=../dataset/test_sampled_0_500.txt \
#     --test_data_file=../dataset/test_sampled.txt \
#     --block_size 512 \
#     --eval_batch_size 32 \
#     --num_of_changes 2 \
#     --seed 123456


#attack_mhm
# CUDA_VISIBLE_DEVICES=0 python attack_mhm.py \
#     --output_dir=./saved_models \
#     --model_type=roberta \
#     --tokenizer_name=microsoft/codebert-base \
#     --model_name_or_path=microsoft/codebert-base \
#     --csv_store_path ./attack_mhm.csv \
#     --base_model=microsoft/codebert-base-mlm \
#     --train_data_file=../dataset/train_sampled.txt \
#     --eval_data_file=../dataset/test_sampled_0_500.txt \
#     --test_data_file=../dataset/test_sampled.txt \
#     --block_size 512 \
#     --eval_batch_size 64 \
#     --seed 123456


#attack_alert
# CUDA_VISIBLE_DEVICES=0 python attack_alert.py \
#     --output_dir=./saved_models \
#     --model_type=roberta \
#     --config_name=microsoft/codebert-base \
#     --csv_store_path ./attack_alert.csv \
#     --model_name_or_path=microsoft/codebert-base \
#     --tokenizer_name=roberta-base \
#     --base_model=microsoft/codebert-base-mlm \
#     --train_data_file=../dataset/train_sampled.txt \
#     --eval_data_file=../dataset/test_sampled_0_500.txt \
#     --test_data_file=../dataset/test_sampled.txt \
#     --block_size 512 \
#     --eval_batch_size 32 \
#     --seed 123456