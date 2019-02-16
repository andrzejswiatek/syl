from drawing import painting
from prodline import processing

processor_factory =  processing.ProcessorFactory()
serialize_file = 'D:\\Repositories\\GITSYL\\syl\\values.pickle'
input_file = r'D:\Projekty\MachineLearning\Sylwek\tasma.mp4'

processor = processor_factory.create()
painter = painting.Painter('Monitoring linii produkcyjnej', serialize_file, processor)
video_processor = processing.VideoProcessor(input_file, processor, painter)

with video_processor:
    video_processor.process()

