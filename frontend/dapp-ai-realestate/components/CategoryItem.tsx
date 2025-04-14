import Image from 'next/image';
import Link from 'next/link';

interface CategoryItemProps {
  image: string;
  title: string;
}

export default function CategoryItem({ image, title }: CategoryItemProps) {
  return (
    <div className="flex flex-col md:flex-row border p-1">
      <div className="w-full md:w-7/12">
        <Link href="#" className="block">
          <div className="relative w-full h-48">
            <Image 
              src={image} 
              alt={title} 
              fill
              className="object-cover"
            />
          </div>
        </Link>
      </div>
      <div className="w-full md:w-5/12 flex items-center">
        <Link href="#" className="w-full py-3 text-center hover:bg-gray-100">
          {title}
        </Link>
      </div>
    </div>
  );
}
