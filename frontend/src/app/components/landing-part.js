import Image from 'next/image';
import '../styles/landing-styles.css';
import BookImage from '../images/glasses-book.jpg';

export default function LandingPart() {
    return (
     <div className='content-container'>
      <div className='introduce'>
        <div className='big-text-section introduce-text'>
          <p className='intro-text-first'>We create</p>
          <p className='intro-text-second'>quotes like</p>
          <p className='intro-text-third'>a pro & more</p>
          <p className='intro-text-quad'>efficient</p>
        </div>
        <p className='text-section'>An innovative solution for those who 
          are looking for inspiration and want to share wisdom with othe
          rs. Advanced artificial intelligence technologies to offer you
          unique and original quotes on any topic.</p>

        <div className='post-introduce-image-block'>
        <Image src={ BookImage } alt='glasses-image' width={500} height={300} 
        className='custom-book-image'/>
       </div>

       <div className='bottom-text-container'>
        <div className='slogan'>
          <p className='slogan-text-first'>Motivation, love,</p>
          <p className='slogan-text-second'>success or</p>
          <p className='slogan-text-third'>philosophy</p>
          <p className='slogan-text-quad'>-we have quotes</p>
          <p className='slogan-text-five'>that are     need</p>
          <p className='slogan-text-six'>for any time</p>
        </div>
        <p className='bottom-text-section'>Each quote is generated using 
          algorithms that ensure originality. You can be sure that your 
          quotes are not repeated and stand out from others.</p>
       </div>
      </div>
     </div>
  );
}