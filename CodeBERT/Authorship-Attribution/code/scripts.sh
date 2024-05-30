#train
python run.py \
    --output_dir=./saved_models/gcjpy \
    --model_type=roberta \
    --config_name=microsoft/codebert-base \
    --model_name_or_path=microsoft/codebert-base \
    --tokenizer_name=roberta-base \
    --number_labels 66 \
    --do_train \
    --train_data_file=../dataset/data_folder/processed_gcjpy/train.txt \
    --eval_data_file=../dataset/data_folder/processed_gcjpy/valid.txt \
    --test_data_file=../dataset/data_folder/processed_gcjpy/valid.txt \
    --epoch 30 \
    --block_size 512 \
    --train_batch_size 16 \
    --eval_batch_size 32 \
    --learning_rate 5e-5 \
    --max_grad_norm 1.0 \
    --evaluate_during_training \
    --seed 123456


#eval_asr
# CUDA_VISIBLE_DEVICES=0 python run.py \
#     --output_dir=./saved_models/gcjpy \
#     --model_type=roberta \
#     --config_name=microsoft/codebert-base \
#     --model_name_or_path=microsoft/codebert-base \
#     --tokenizer_name=roberta-base \
#     --do_asr \
#     --number_labels 66 \
#     --train_data_file=../dataset/data_folder/processed_gcjpy/train.txt \
#     --eval_data_file=../dataset/data_folder/processed_gcjpy/valid.txt \
#     --test_data_file=../dataset/data_folder/processed_gcjpy/valid.txt \
#     --adv_data_file=./advs/adv_codebert_ours_unused_function_arguments_attack_untargeted_ablation_num_of_changes_2.txt \
#     --block_size 512 \
#     --train_batch_size 16 \
#     --eval_batch_size 32 \
#     --seed 123456


#attack
# CUDA_VISIBLE_DEVICES=0 python attack_ablation_ensemble.py \
#     --output_dir=./saved_models/gcjpy \
#     --model_type=roberta \
#     --config_name=microsoft/codebert-base \
#     --model_name_or_path=microsoft/codebert-base \
#     --tokenizer_name=roberta-base \
#     --number_labels 66 \
#     --do_eval \
#     --csv_store_path ./attack_gi.csv \
#     --language_type python \
#     --train_data_file=../dataset/data_folder/processed_gcjpy/train.txt \
#     --eval_data_file=../dataset/data_folder/processed_gcjpy/valid.txt \
#     --test_data_file=../dataset/data_folder/processed_gcjpy/valid.txt \
#     --block_size 512 \
#     --train_batch_size 8 \
#     --eval_batch_size 32 \
#     --evaluate_during_training \
#     --num_of_changes 2 \
#     --seed 123456


#attack_nsga
# CUDA_VISIBLE_DEVICES=0 python attack_ablation_ensemble_nsga.py \
#     --output_dir=./saved_models/gcjpy \
#     --model_type=roberta \
#     --config_name=microsoft/codebert-base \
#     --model_name_or_path=microsoft/codebert-base \
#     --tokenizer_name=roberta-base \
#     --number_labels 66 \
#     --do_eval \
#     --csv_store_path ./attack_gi.csv \
#     --language_type python \
#     --train_data_file=../dataset/data_folder/processed_gcjpy/train.txt \
#     --eval_data_file=../dataset/data_folder/processed_gcjpy/valid.txt \
#     --test_data_file=../dataset/data_folder/processed_gcjpy/valid.txt \
#     --block_size 512 \
#     --train_batch_size 8 \
#     --eval_batch_size 32 \
#     --evaluate_during_training \
#     --num_of_changes 2 \
#     --seed 123456


#attack_mhm
# CUDA_VISIBLE_DEVICES=0 python attack_mhm.py \
#     --output_dir=./saved_models/gcjpy \
#     --model_type=roberta \
#     --config_name=microsoft/codebert-base \
#     --model_name_or_path=microsoft/codebert-base \
#     --tokenizer_name=roberta-base \
#     --cache_dir=../cache/microsoft/codebert-base \
#     --number_labels 66 \
#     --do_eval \
#     --csv_store_path ./attack_gi.csv \
#     --language_type python \
#     --train_data_file=../dataset/data_folder/processed_gcjpy/train.txt \
#     --eval_data_file=../dataset/data_folder/processed_gcjpy/valid.txt \
#     --test_data_file=../dataset/data_folder/processed_gcjpy/valid.txt \
#     --block_size 512 \
#     --train_batch_size 8 \
#     --eval_batch_size 32 \
#     --evaluate_during_training \
#     --seed 123456


#attack_alert
# CUDA_VISIBLE_DEVICES=0 python attack_alert.py \
#     --output_dir=./saved_models/gcjpy \
#     --model_type=roberta \
#     --config_name=microsoft/codebert-base \
#     --model_name_or_path=microsoft/codebert-base \
#     --tokenizer_name=roberta-base \
#     --cache_dir=../cache/microsoft/codebert-base \
#     --number_labels 66 \
#     --do_eval \
#     --csv_store_path ./attack_gi.csv \
#     --language_type python \
#     --train_data_file=../dataset/data_folder/processed_gcjpy/train.txt \
#     --eval_data_file=../dataset/data_folder/processed_gcjpy/valid.txt \
#     --test_data_file=../dataset/data_folder/processed_gcjpy/valid.txt \
#     --block_size 512 \
#     --train_batch_size 8 \
#     --eval_batch_size 32 \
#     --evaluate_during_training \
#     --seed 123456