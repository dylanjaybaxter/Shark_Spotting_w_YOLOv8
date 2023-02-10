import torch #For Checking the Card
import utils # for downloading models/datasets

# Show Card
print('torch %s %s' % (torch.__version__, torch.cuda.get_device_properties(0) if torch.cuda.is_available() else 'CPU'))

