# pre-processing the data
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.impute import SimpleImputer 
import sys
from dataclasses import dataclass 
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer 
import os
from src.exception import CustomException 
from src.logger import logging 
from sklearn.pipeline import Pipeline
from src.utils import save_object
#from src.components.data_ingestion import DataIngestion
from src.utils import save_object


@dataclass 
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts','preprocessor.pkl')

# creating all these functions as a pickle files
class DataTransformation:
    def __init__(self) -> None:
        self.data_transformation = DataTransformationConfig() 
    
    def get_data_transformationObj(self):
        try:
            numerical_columns = ['writing_score','reading_score']
            categorical_columns = ['gender','race_ethnicity','parental_level_of_education',
                                   'lunch','test_preparation_course']
            
            num_pipeline = Pipeline(
                steps=[
                ('imputer',SimpleImputer(strategy='median')),
                ('Scaler',StandardScaler()),
                ]
            )

            cat_pipeline = Pipeline(
                steps=[
                ("imputer",SimpleImputer(strategy='most_frequent')),
                ('one_hot_encoder',OneHotEncoder()),
                ('Scaler',StandardScaler(with_mean=False)),
                ]
            )

            logging.info('NUmerical and CATEGORICAL COLUMSN TRSNFORMATION DONE ....')

            # why should we use column transformer ?
            preprocessor = ColumnTransformer(
                    [
                        ('num_pipelime',num_pipeline,numerical_columns),
                        ('cat_pipeline',cat_pipeline,categorical_columns)
                    ]

            )

            return preprocessor 
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info('Read the train and test data completed') 
            preprocessing_obj = self.get_data_transformationObj() 
            target_column_name = "math_score" 
            numerical_columns = ['writing_score','reading_score'] 

            input_feature_train_df = train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info(
                f'Applying pre-processing steps on the train and test data'
            )

            input_feature_train_Arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_Arr = preprocessing_obj.transform(input_feature_test_df) 

            # adds the column across the axis 
            '''
                [[
                    1,4
                    2,5
                    3,6
                ]]
            '''
            train_arr = np.c_[input_feature_train_Arr , np.array(target_feature_train_df)] 
            test_arr = np.c_[input_feature_test_Arr, np.array(target_feature_test_df)]

            logging.info(f'completed the preprocessing steps and saving the objects path')


            save_object(
                filepath = self.data_transformation.preprocessor_obj_file_path,
                obj = preprocessing_obj
            )

            return(
                train_arr,
                test_arr,
                self.data_transformation.preprocessor_obj_file_path
            )
        except Exception as e:
            raise CustomException(e,sys) 
        
 
