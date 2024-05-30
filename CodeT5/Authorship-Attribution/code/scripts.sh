#train
CUDA_VISIBLE_DEVICES=0 python run.py \
    --output_dir=./saved_models/gcjpy \
    --model_type=t5 \
    --config_name=Salesforce/codet5-base \
    --model_name_or_path=Salesforce/codet5-base \
    --tokenizer_name=codet5-base \
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
# CUDA_VISIBLE_DEVICES=5 python run.py \
#     --output_dir=./saved_models/gcjpy \
#     --model_type=t5 \
#     --config_name=Salesforce/codet5-base \
#     --model_name_or_path=Salesforce/codet5-base \
#     --tokenizer_name=codet5-base \
#     --number_labels 66 \
#     --do_asr \
#     --train_data_file=../dataset/data_folder/processed_gcjpy/train.txt \
#     --eval_data_file=../dataset/data_folder/processed_gcjpy/valid.txt \
#     --test_data_file=../dataset/data_folder/processed_gcjpy/valid.txt \
#     --adv_data_file=./advs_transfer/adv_codebert_ours_insert_comments_attack_untargeted_ablation_num_of_changes_2.txt \
#     --epoch 30 \
#     --block_size 512 \
#     --train_batch_size 16 \
#     --eval_batch_size 1 \
#     --learning_rate 5e-5 \
#     --max_grad_norm 1.0 \
#     --evaluate_during_training \
#     --seed 123456



#attack
# CUDA_VISIBLE_DEVICES=0 python attack_ablation_ensemble.py \
#     --output_dir=./saved_models/gcjpy \
#     --model_type=t5 \
#     --config_name=Salesforce/codet5-base \
#     --model_name_or_path=Salesforce/codet5-base \
#     --tokenizer_name=codet5-base \
#     --number_labels 66 \
#     --do_eval \
#     --csv_store_path ./attack_gi.csv \
#     --language_type python \
#     --train_data_file=../dataset/data_folder/processed_gcjpy/train.txt \
#     --eval_data_file=../dataset/data_folder/processed_gcjpy/train.txt \
#     --test_data_file=../dataset/data_folder/processed_gcjpy/valid.txt \
#     --block_size 512 \
#     --train_batch_size 8 \
#     --eval_batch_size 32 \
#     --evaluate_during_training \
#     --num_of_changes 2 \
#     --seed 123456
