FORWARD = 'CREATE CONSTRAINT unique_sample_name ON (a:SampleNode) ASSERT a.name IS UNIQUE'
BACKWARD = 'DROP CONSTRAINT unique_sample_name'
