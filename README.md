# iMusic-Player
An intellegent Music Player made in Python using the <a href="http://librosa.github.io/librosa/">Librosa</a> music libarary.

The basic idea of the program is to maintain unique user profiles and recommend the next song to the user in real time with no reliance on song metadata. Instead, the user's habits and preferences are learnt over time.

The program uses content based filtering by extracting raw data from music files in the form of Mel Frequency Cepstral Coefficients (MFCCs). The MFCCs are a feature matrix modeled as a Gaussian distribution. The similarity between each distribution is measured as a distance metric given by K-L Divergence.

The general working of the program is shown below:
![alt=basic_idea_img](https://github.com/ad8454/iMusic-Player/blob/master/iMusicBasicIdea.JPG)

The user can Like or Dislike the currently playing song and influence the recommendations in the future.
