#train
CUDA_VISIBLE_DEVICES=0 python run.py \
    --output_dir=./saved_models/gcjpy \
    --config_name=microsoft/graphcodebert-base \
    --model_name_or_path=microsoft/graphcodebert-base \
    --tokenizer_name=microsoft/graphcodebert-base \
    --do_train \
    --language_type python \
    --number_labels 66 \
    --train_data_file=../dataset/data_folder/processed_gcjpy/train.txt \
    --eval_data_file=../dataset/data_folder/processed_gcjpy/valid.txt \
    --test_data_file=../dataset/data_folder/processed_gcjpy/test.txt \
    --epoch 30 \
    --code_length 384 \
    --data_flow_length 128 \
    --train_batch_size 16 \
    --eval_batch_size 32 \
    --learning_rate 2e-5 \
    --max_grad_norm 1.0 \
    --evaluate_during_training \
    --seed 123456


#eval_asr
# CUDA_VISIBLE_DEVICES=5 python run.py \
#     --output_dir=./saved_models/gcjpy \
#     --config_name=microsoft/graphcodebert-base \
#     --model_name_or_path=microsoft/graphcodebert-base \
#     --tokenizer_name=microsoft/graphcodebert-base \
#     --do_asr \
#     --language_type python \
#     --number_labels 66 \
#     --train_data_file=../dataset/data_folder/processed_gcjpy/train.txt \
#     --eval_data_file=../dataset/data_folder/processed_gcjpy/valid.txt \
#     --test_data_file=../dataset/data_folder/processed_gcjpy/test.txt \
#     --adv_data_file=./advs_transfer/adv_codebert_ours_insert_comments_attack_untargeted_ablation_num_of_changes_2.txt \
#     --epoch 30 \
#     --code_length 384 \
#     --data_flow_length 128 \
#     --train_batch_size 16 \
#     --eval_batch_size 1 \
#     --learning_rate 2e-5 \
#     --max_grad_norm 1.0 \
#     --evaluate_during_training \
#     --seed 123456


#attack
# CUDA_VISIBLE_DEVICES=0 python attack_ablation_ensemble.py \
#     --output_dir=./saved_models/gcjpy \
#     --model_type=roberta \
#     --tokenizer_name=microsoft/graphcodebert-base \
#     --model_name_or_path=microsoft/graphcodebert-base \
#     --csv_store_path ./attack_no_gi.csv \
#     --language_type python \
#     --number_labels 66 \
#     --train_data_file=../dataset/data_folder/processed_gcjpy/train.txt \
#     --eval_data_file=../dataset/data_folder/processed_gcjpy/train.txt \
#     --test_data_file=../dataset/data_folder/processed_gcjpy/test.txt \
#     --code_length 384 \
#     --data_flow_length 128 \
#     --eval_batch_size 32 \
#     --num_of_changes 2 \
#     --seed 123456