from function import *
# from keras.utils import to_categorical
from keras.models import model_from_json
# from keras.layers import LSTM, Dense
# from keras.callbacks import TensorBoard
import pyttsx3

json_file = open("model.json", "r")
model_json = json_file.read()
json_file.close()
model = model_from_json(model_json)
model.load_weights("model.h5")

colors = []
for i in range(0,20):
    colors.append((245,117,16))
    
def say_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    
def prob_viz(res, actions, input_frame, colors,threshold):
    output_frame = input_frame.copy()
    for num, prob in enumerate(res):
        cv2.rectangle(output_frame, (0,60+num*40), (int(prob*100), 90+num*40), colors[num], -1)
        cv2.putText(output_frame, actions[num], (0, 85+num*40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
        
    return output_frame

sequence = []
sentence = []
accuracy=[]
predictions = []
threshold = 0.8 

cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    while cap.isOpened():

        ret, frame = cap.read()
        cropframe=frame[40:400,0:300]
        frame=cv2.rectangle(frame,(0,40),(300,400),255,2)
        image, results = mediapipe_detection(cropframe, hands)

        keypoints = extract_keypoints(results)
        sequence.append(keypoints)
        sequence = sequence[-30:]
        
        # print(len(sequence))

        try: 
            if len(sequence) == 30:
                res = model.predict(np.expand_dims(sequence, axis=0))[0]
                predictions.append(np.argmax(res))
                # print(res)
   
                if np.unique(predictions[-10:])[0]==np.argmax(res): 
                    if res[np.argmax(res)] > threshold: 
                        acc = res[np.argmax(res)] * 100
                        # print("Accuracy:", acc)
                        if(acc>99.9):
                            print("Good to see you")
                            text = "Good to see you"
                            say_text(text)
                            
    #                     elif(acc>96.0):
    #                         print("Hey! How are you")
    #                         text = "Hey! How are you"
    #                         say_text(text)
                            
    #                     elif(acc>93.0):
    #                         print("You look great today")
    #                         text = "You look great today"
    #                         say_text(text)
                            
    #                     elif(acc>91.0):
    #                         print("Hey! How are you")
    #                         text = "Could you tell me the way to the nearest washroom?"
    #                         say_text(text)
                            
    #                     elif(acc>89.0):
    #                         print("Thank you so much")
    #                         text = "Thank you so much"
    #                         say_text(text)
                            
    #                     elif(acc>86.0):
    #                         print("Hey! How are you")
    #                         text = "The weather's great today"
    #                         say_text(text)
                            
                        elif(acc>82.0):
                            print("Hey! How are you")
                            text = "A medium cup of tea please"
                            say_text(text)
                            
                        else:
                            print("Could you help me cross the road please?")
                            text = "Could you help me cross the road please?"
                            say_text(text)
                            
                    if len(sentence) > 0: 
                        if actions[np.argmax(res)] != sentence[-1]:
                            sentence.append(actions[np.argmax(res)])
                            accuracy.append(str(res[np.argmax(res)]*100))

                        else:
                            sentence.append(actions[np.argmax(res)])
                            accuracy.append(str(res[np.argmax(res)]*100)) 

                    if len(sentence) > 1: 
                        sentence = sentence[-1:]
                        accuracy=accuracy[-1:]
                            
        except Exception as e:
            pass
            
        cv2.rectangle(frame, (0,0), (300, 40), (245, 117, 16), -1)
        cv2.putText(frame,"Output: -"+' '.join(sentence)+''.join(accuracy), (3,30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow('OpenCV Feed', frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        
    cap.release()
    # cv2.destroyAllWindows()