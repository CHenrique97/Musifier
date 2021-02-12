import torch
import json,re,os
import torch.nn as nn
import string
import random
import sys
import music21  

from torch.utils.tensorboard import SummaryWriter
# Device configuration
print("cuda" if torch.cuda.is_available() else "cpu")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# Get characters from string.printable
all_characters = string.printable
n_characters = len(all_characters)

# Read large text file (Note can be any text file: not limited to just names)



class RNN(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(RNN, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        self.embed = nn.Embedding(input_size, hidden_size)
        self.lstm = nn.LSTM(hidden_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x, hidden, cell):
        out = self.embed(x)
        out, (hidden, cell) = self.lstm(out.unsqueeze(1), (hidden, cell))
        out = self.fc(out.reshape(out.shape[0], -1))
        return out, (hidden, cell)

    def init_hidden(self, batch_size):
        hidden = torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device)
        cell = torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device)
        return hidden, cell


class Generator:
    def __init__(self):
        self.chunk_len = 500
        self.num_epochs = 3000
        self.batch_size = 1
        self.print_every = 50
        self.hidden_size = 256
        self.num_layers = 5
        self.lr = 0.003

    def char_tensor(self, string):
        tensor = torch.zeros(len(string)).long()
        for c in range(len(string)):
            tensor[c] = all_characters.index(string[c])
        return tensor



    def generate(self, initial_str='{"note":', predict_len=5000, temperature=0.95):
        hidden, cell = self.rnn.init_hidden(batch_size=self.batch_size)
        initial_input = self.char_tensor(initial_str)
        predicted = initial_str

        for p in range(len(initial_str) - 1):
            _, (hidden, cell) = self.rnn(
                initial_input[p].view(1).to(device), hidden, cell
            )

        last_char = initial_input[-1]

        for p in range(predict_len):
            output, (hidden, cell) = self.rnn(
                last_char.view(1).to(device), hidden, cell
            )
            output_dist = output.data.view(-1).div(temperature).exp()
            top_char = torch.multinomial(output_dist, 1)[0]
            predicted_char = all_characters[top_char]
            predicted += predicted_char
            last_char = self.char_tensor(predicted_char)

        return predicted


    
Generator=torch.load('pianoRock.pth')
beggining='{"score-partwise":{"$":{"version":"3.1"},"part-list":{"score-part":{"$":{"id":"P1"},"part-name":"Generic Intrument","part-abbreviation":"GEn IN.","score-instrument":{"$":{"id":"P1-I1"},"instrument-name":"Piano"},"midi-device":{"$":{"id":"P1-I1","port":"1"}},"midi-instrument":{"$":{"id":"P1-I1"},"midi-channel":"1","midi-program":"01","volume":"100","pan":"0"}}},"part":{"$":{"id":"P1"},"measure":{"$":{"number":"1"},"attributes": {"divisions": "480","key": {"fifths":"0"},"time": {"beats": "4","beat-type": "4" },"clef": {"sign": "G","line": "2","clef-octave-change": "-1"} },'
middle=''
end='}}}}'
dataGen=Generator.generate()
print(dataGen)
dataSplit=dataGen.split(':')
notesSplit=[]
dataGen=dataGen.replace('"','').replace('{','/').replace('},','/').replace(',','/').replace(' ','')
dataSplit=dataGen.split('/')
dataList=[]

for k in range(len(dataSplit)):
    notesDict={}
    try:
        if ('pitch' in dataSplit[k]):
            notesDict['pitch']={}
            if ('step' in dataSplit[k+1] or 'octave' in dataSplit[k+1] or 'alter' in dataSplit[k+1]):
                notesDict['pitch'][dataSplit[k+1].split(':')[0]]=dataSplit[k+1].split(':')[1]
            if ('step' in dataSplit[k+2] or 'octave' in dataSplit[k+2] or 'alter' in dataSplit[k+2]):
                notesDict['pitch'][dataSplit[k+2].split(':')[0]]=dataSplit[k+2].split(':')[1]
            if ('step' in dataSplit[k+3] or 'octave' in dataSplit[k+3] or 'alter' in dataSplit[k+3]):
                notesDict['pitch'][dataSplit[k+3].split(':')[0]]=dataSplit[k+3].split(':')[1] 
            if ('duration' in dataSplit[k+3] ):
                notesDict['duration']=dataSplit[k+3].split(':')[1]
                #
            if ('duration' in dataSplit[k+4] or 'voice' in dataSplit[k+4] ):
                notesDict[dataSplit[k+4].split(':')[0]]=dataSplit[k+4].split(':')[1].replace('}]','')   
            if ('duration' in dataSplit[k+5] or 'voice' in dataSplit[k+5] ):
                notesDict[dataSplit[k+5].split(':')[0]]=dataSplit[k+5].split(':')[1].replace('}]','')
#            if ('duration' in dataSplit[k+6] or 'voice' in dataSplit[k+6] or 'type' in dataSplit[k+6] ):
#                if ('32nd' in dataSplit[k+6].split(':')[1].replace('}]','') or 'whole' in dataSplit[k+6].split(':')[1].replace('}]','') or 'quarter' in dataSplit[k+6].split(':')[1].replace('}]','') ):
#                    notesDict[dataSplit[k+6].split(':')[0]]='eighth'
#                else:      
#                    notesDict[dataSplit[k+6].split(':')[0]]=dataSplit[k+6].split(':')[1].replace('}]','')                  
            dataList.append(notesDict)

    except:
        pass

middle=json.dumps({'note':dataList+dataList+dataList})
with open('tempFile.json', 'w') as f:

    json.dump(json.loads(beggining+middle[1:-1]+end),f)

os.system('cmd /c "node converter.js"')
print()

os.system('cmd /c "move '+str(music21.converter.parse('tempFile2.xml').write('midi'))+'  song.mid "')

